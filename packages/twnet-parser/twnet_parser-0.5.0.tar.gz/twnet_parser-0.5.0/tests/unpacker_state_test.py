from twnet_parser.packer import Unpacker, pack_int, pack_str
from twnet_parser.packer import \
        NO_SANITIZE, SANITIZE, SANITIZE_CC, SKIP_START_WHITESPACES

def test_unpack_ints_and_strings() -> None:
    u = Unpacker(b'\x01\x02\x03\x01foo\x00bar\x00')
    assert u.get_int() == 1
    assert u.get_int() == 2
    assert u.get_int() == 3
    assert u.get_int() == 1
    assert u.get_str() == 'foo'
    assert u.get_str() == 'bar'

def test_pack_bools() -> None:
    assert pack_int(False) == b'\x00'
    assert pack_int(True) == b'\x01'

    assert pack_int(0) == b'\x00'
    assert pack_int(1) == b'\x01'

def test_unpack_bools() -> None:
    data: bytes = b'\x00\x01'
    u = Unpacker(data)
    assert (u.get_int() == 1) is False
    assert (u.get_int() == 1) is True

def test_simple_repack() -> None:
    data: bytes = pack_str('hello world')
    assert data == b'hello world\x00'
    data += pack_int(22)

    u = Unpacker(data)
    assert u.get_str() == 'hello world'
    assert u.get_int() == 22

def test_non_ascii_repack() -> None:
    data: bytes = pack_str('💩')
    assert data == '💩'.encode('utf-8') + b'\x00'

    u = Unpacker(data)
    assert u.get_str() == '💩'

def test_string_sanitize_should_not_affect_plain_ascii():
    u = Unpacker(b'\x41\x41\x00\x42\x42\x00\x42\x42\x00\x42\x42\x00')
    assert u.get_str(NO_SANITIZE) == 'AA'
    assert u.get_str(SANITIZE) == 'BB'
    assert u.get_str(SANITIZE_CC) == 'BB'
    assert u.get_str(SKIP_START_WHITESPACES) == 'BB'
    assert u.get_str() == ''

def test_string_no_sanitize_keep_space():
    u = Unpacker(b'\x20\x41\x41\x00')
    assert u.get_str(NO_SANITIZE) == ' AA'

def test_string_no_sanitize_should_not_crash_on_invalid_utf8():
    u = Unpacker(b'\x80\n\x41\x41\n\x00')
    assert u.get_str(NO_SANITIZE) == '\nAA\n'

def test_string_no_sanitize_keep_newline():
    u = Unpacker(b'\n\x41\x41\n\x00')
    assert u.get_str(NO_SANITIZE) == '\nAA\n'

def test_string_no_sanitize_keep_r_and_t():
    u = Unpacker(b'\r\x41\x41\t\x00')
    assert u.get_str(NO_SANITIZE) == '\rAA\t'

def test_string_sanitize_keep_r_and_t():
    u = Unpacker(b'\r\x41\x41\t\x00')
    assert u.get_str(SANITIZE) == '\rAA\t'

def test_string_sanitize_by_default_keep_r_and_t():
    u = Unpacker(b'\r\x41\x41\t\x00')
    assert u.get_str() == '\rAA\t'

def test_string_sanitize_strip_x01_x02():
    u = Unpacker(b'\x41\x01\x02\x41\x00')
    assert u.get_str(SANITIZE) == 'A  A'

def test_string_sanitize_cc_strip_r_and_t():
    u = Unpacker(b'\x41\x01\x02\x41\x00')
    assert u.get_str(SANITIZE_CC) == 'A  A'
    u = Unpacker(b'\r\x41\x41\t\x00')
    assert u.get_str(SANITIZE_CC) == ' AA '
    u = Unpacker(b'\r\t\r\r\r\x00')
    assert u.get_str(SANITIZE_CC) == '     '

def test_string_sanitize_cc_strip_x01_x02():
    u = Unpacker(b'\x01\x02\x00')
    assert u.get_str(SANITIZE_CC) == '  '
    u = Unpacker(b'foo\x01bar\x02\x01baz\x00')
    assert u.get_str(SANITIZE_CC) == 'foo bar  baz'

# TODO: should we strip that? Do not think so since tw is full of unicode
#       only single bytes lower than 32 are stripped
#       but multi byte unicode with bytes over 32 should be fine
# def test_string_sanitize_cc_strip_poop_emoji():
#     u = Unpacker('💩'.encode('utf-8') + b'\x00')
#     assert u.get_str(SANITIZE_CC) == len('💩'.encode('utf-8')) * ' '
#     u = Unpacker(b'foo' + '💩'.encode('utf-8') + b'bar\x00')
#     assert u.get_str(SANITIZE_CC) == f"foo{len('💩'.encode('utf-8')) * ' '}bar"

def test_string_sanitize_cc_keep_poop_emoji():
    u = Unpacker('💩'.encode('utf-8') + b'\x00')
    assert u.get_str(SANITIZE_CC) == '💩'
    u = Unpacker(b'foo' + '💩'.encode('utf-8') + b'bar\x00')
    assert u.get_str(SANITIZE_CC) == 'foo💩bar'

def test_string_sanitize_keep_poop_emoji():
    u = Unpacker('💩'.encode('utf-8') + b'\x00')
    assert u.get_str(SANITIZE) == '💩'
    u = Unpacker(b'foo' + '💩'.encode('utf-8') + b'bar\x00')
    assert u.get_str(SANITIZE) == 'foo💩bar'

def test_string_no_sanitize_keep_poop_emoji():
    u = Unpacker('💩'.encode('utf-8') + b'\x00')
    assert u.get_str(NO_SANITIZE) == '💩'
    u = Unpacker(b'foo' + '💩'.encode('utf-8') + b'bar\x00')
    assert u.get_str(NO_SANITIZE) == 'foo💩bar'

def test_string_skip_start_whitespaces_strip_leading_spaces():
    u = Unpacker(b'          \x00')
    assert u.get_str(SKIP_START_WHITESPACES) == ''
    u = Unpacker(b'\t \t        \t        foo bar \t baz\x00')
    assert u.get_str(SKIP_START_WHITESPACES) == 'foo bar \t baz'

# TODO: check tw code what this should do
# def test_string_skip_start_whitespaces_strip_x01_x02():
#     """
#     https://chillerdragon.github.io/teeworlds-protocol/07/fundamentals.html#string_packing
#
#     UB in this spec :shrug:
#     """
#     u = Unpacker(b'\x01\x02\x00')
#     assert u.get_str(SKIP_START_WHITESPACES) == ''
#     u = Unpacker(b'\tfoo\x01bar\x02\x01baz\x00')
#     assert u.get_str(SKIP_START_WHITESPACES) == 'foo bar  baz'

def test_raw_repack_at_end() -> None:
    data: bytes = b''
    data += pack_int(1)
    data += pack_str('a')
    data += b'rawr'

    u = Unpacker(data)
    assert u.get_int() == 1
    assert u.get_str() == 'a'
    assert u.get_raw() == b'rawr'

def test_raw_sized_repack() -> None:
    data: bytes = b''
    data += pack_int(1)
    data += pack_str('a')
    data += b'rawr'
    data += b'abc'
    data += b'\x00\x00'
    data += b'\x01\x02'
    data += pack_int(1)
    data += pack_int(2)
    data += b'\x00\x00'

    u = Unpacker(data)
    assert u.get_int() == 1
    assert u.get_str() == 'a'
    assert u.get_raw(4) == b'rawr'
    assert u.get_raw(3) == b'abc'
    assert u.get_raw(2) == b'\x00\x00'
    assert u.get_raw(2) == b'\x01\x02'
    assert u.get_int() == 1
    assert u.get_int() == 2
    assert u.get_raw(2) == b'\x00\x00'

def test_multi_repack() -> None:
    strs: list[str] = [
            'foo',
            'bar',
            'baz',
            '',
            'yeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeeeeeeeeeeeeeeeeee' \
            'eeeppiiiiiiiiiiiiiii',
            'a b c d e f',
            'nameless tee',
            '(1)nameless tee',
            '[D](1)nameless t']

    ints: list[int] = [
            0,
            111111111,
            222222222,
            649010,
            -1,
            -19882,
            29299]

    # pack
    data: bytes = b''
    for string in strs:
        data += pack_str(string)
    for num in ints:
        data += pack_int(num)

    # unpack
    u = Unpacker(data)
    for string in strs:
        assert u.get_str() == string
    for num in ints:
        assert u.get_int() == num
