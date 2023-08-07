from twnet_parser.packet import \
    parse7, PacketHeaderParser7, PacketHeader, TwPacket

def test_packet_header_unpack() -> None:
    # TODO: change api to
    #       PacketHeader.pack()
    #       PacketHeader.unpack(bytes)

    parser = PacketHeaderParser7()
    header: PacketHeader = parser.parse_header(b'\x04\x0a\x00\xcf\x2e\xde\x1d')

    assert header.ack == 10
    assert header.token == b'\xcf.\xde\x1d'
    assert header.num_chunks == 0

    assert header.flags.control is True
    assert header.flags.resend is False
    assert header.flags.compression is False
    assert header.flags.connless is False

def test_packet_header_pack_flags() -> None:
    header: PacketHeader = PacketHeader()
    header.ack = 0

    header.flags.control = True
    header.flags.resend = False
    header.flags.compression = False
    header.flags.connless = False
    assert header.pack()[0:1] == b'\x04'

    header.flags.control = False
    header.flags.resend = False
    header.flags.compression = True
    header.flags.connless = False
    assert header.pack()[0:1] == b'\x10'

def test_packet_header_pack_ack() -> None:
    header: PacketHeader = PacketHeader()
    header.flags.control = False
    header.flags.resend = False
    header.flags.compression = False
    header.flags.connless = False

    header.ack = 8
    assert header.pack()[1:2] == b'\x08'
    header.ack = 9
    assert header.pack()[1:2] == b'\x09'
    header.ack = 10
    assert header.pack()[1:2] == b'\x0a'
    header.ack = 11
    assert header.pack()[1:2] == b'\x0b'

def test_packet_header_repack_overflowing_ack() -> None:
    header: PacketHeader = PacketHeader()
    header.flags.control = False
    header.flags.resend = False
    header.flags.compression = False
    header.flags.connless = False

    header.ack = 1024
    parser = PacketHeaderParser7()
    header = parser.parse_header(header.pack())
    assert header.ack == 0

    header.ack = 1025
    parser = PacketHeaderParser7()
    header = parser.parse_header(header.pack())
    assert header.ack == 1

    header.ack = 2000
    parser = PacketHeaderParser7()
    header = parser.parse_header(header.pack())
    assert header.ack == 976

def test_packet_header_repack_ack_overlapping_into_flags_byte() -> None:
    header: PacketHeader = PacketHeader()
    header.flags.control = False
    header.flags.resend = False
    header.flags.compression = False
    header.flags.connless = False

    parser = PacketHeaderParser7()

    header.ack = 8
    assert header.pack()[0:2] == b'\x00\x08'

    data = header.pack()
    header = parser.parse_header(data)
    assert header.ack == 8

    # https://github.com/teeworlds/teeworlds/blob/26d24ec061d44e6084b2d77a9b8a0a48e354eba6/src/engine/shared/network.h#L112
    # NET_MAX_SEQUENCE = 1<<10
    # which is 1024
    # so ack is being clamped with ack%NET_MAX_SEQUENCE
    # in teeworlds code base
    # meaning 1023 is the highest ack ever sent
    # by official client and server
    header.ack = 1023
    assert header.pack()[0:2] == b'\x03\xff'

    data = header.pack()
    header = parser.parse_header(data)
    assert header.ack == 1023

    # note the first byte being 0x07
    # which is 00000111 in binary
    #          |____/|/
    #          |     |
    #       flags   higher bits of ack
    #
    # usually one sees something like 0x04
    # which is 00000100 where the last two bits are zero
    #
    # so here we do the 2 set bits from 0x07
    # plus all set bits of 0xff
    header = parser.parse_header(b'\x07\xff\x00\xcf\x2e\xde\x1d')
    assert header.ack == 1023
    header = parser.parse_header(b'\x07\xfe\x00\xcf\x2e\xde\x1d')
    assert header.ack == 1022
    header = parser.parse_header(b'\x07\xfd\x00\xcf\x2e\xde\x1d')
    assert header.ack == 1021
    header = parser.parse_header(b'\x07\xfc\x00\xcf\x2e\xde\x1d')
    assert header.ack == 1020
    header = parser.parse_header(b'\x07\xfb\x00\xcf\x2e\xde\x1d')
    assert header.ack == 1019

    # note the first byte being 0x05
    # which is 00000101 in binary
    #          |____/|/
    #          |     |
    #       flags   higher bits of ack
    header = parser.parse_header(b'\x05\xff\x00\xcf\x2e\xde\x1d')
    assert header.ack == 511

def test_packet_header_pack_num_chunks() -> None:
    header = PacketHeader()

    header.num_chunks = 0
    assert header.pack()[2:3] == b'\x00'

    header.num_chunks = 1
    assert header.pack()[2:3] == b'\x01'

    header.num_chunks = 6
    assert header.pack()[2:3] == b'\x06'

def test_packet_header_pack_token() -> None:
    header = PacketHeader()
    header.token = b'\x11\x22\x33\xff'
    assert header.pack()[3:] == b'\x11\x22\x33\xff'

    header.token = b'\x22\xff\xaa\xff'
    assert header.pack()[3:] == b'\x22\xff\xaa\xff'

    header.token = b'\x00\x00\x00\x00'
    assert header.pack()[3:] == b'\x00\x00\x00\x00'

    header.token = b'helo'
    assert header.pack()[3:] == b'helo'

    header.token = b'tekn'
    assert header.pack()[3:] == b'tekn'

def test_packet_header_pack_full() -> None:
    header: PacketHeader = PacketHeader()

    header.ack = 10
    header.token = b'\xcf.\xde\x1d'
    header.num_chunks = 0

    header.flags.control = True
    header.flags.resend = False
    header.flags.compression = False
    header.flags.connless = False

    assert header.pack() == b'\x04\x0a\x00\xcf\x2e\xde\x1d'

def test_packet_header_repack_all_set() -> None:
    header: PacketHeader = PacketHeader()

    header.ack = 1023
    header.token = b'\xff\xff\xff\xff'
    header.num_chunks = 255

    header.flags.control = True
    header.flags.resend = True
    header.flags.compression = True
    header.flags.connless = True

    # Note that even if we set everything
    # we still end up with two leading zeros
    # because those bits are unused
    # and we init the flags with 0
    assert header.pack() == bytes([ \
            0b00111111, \
            0b11111111, \
            0b11111111, \
            0b11111111, \
            0b11111111, \
            0b11111111, \
            0b11111111
    ])

    parser = PacketHeaderParser7()
    header = parser.parse_header(b'\xff\xff\xff\xff\xff\xff\xff')

    assert header.ack == 1023
    assert header.token == b'\xff\xff\xff\xff'
    assert header.num_chunks == 255

    assert header.flags.control is True
    assert header.flags.resend is True
    assert header.flags.compression is True
    assert header.flags.connless is True

    # Note that is doesn matter wether we parse
    #
    # b'\xff\xff\xff\xff\xff\xff\xff'
    #
    #    or
    #
    # b'\x3f\xff\xff\xff\xff\xff\xff'
    #
    # because the first two bytes are ignored anyways
    parser = PacketHeaderParser7()
    header = parser.parse_header(b'\x3f\xff\xff\xff\xff\xff\xff')

    assert header.ack == 1023
    assert header.token == b'\xff\xff\xff\xff'
    assert header.num_chunks == 255

    assert header.flags.control is True
    assert header.flags.resend is True
    assert header.flags.compression is True
    assert header.flags.connless is True

def test_packet_header_repack_none_set() -> None:
    header: PacketHeader = PacketHeader()

    header.ack = 0
    header.token = b'\x00\x00\x00\x00'
    header.num_chunks = 0

    header.flags.control = False
    header.flags.resend = False
    header.flags.compression = False
    header.flags.connless = False

    assert header.pack() == b'\x00\x00\x00\x00\x00\x00\x00'

    parser = PacketHeaderParser7()
    header = parser.parse_header(b'\x00\x00\x00\x00\x00\x00\x00')

    assert header.ack == 0
    assert header.token == b'\x00\x00\x00\x00'
    assert header.num_chunks == 0

    assert header.flags.control is False
    assert header.flags.resend is False
    assert header.flags.compression is False
    assert header.flags.connless is False

def test_parse_7_close() -> None:
    packet: TwPacket = parse7(b'\x04\x0a\x00\xcf\x2e\xde\x1d\04') # 0.7 close

    assert packet.version == '0.7'

    assert packet.header.ack == 10
    assert packet.header.token == b'\xcf.\xde\x1d'
    assert packet.header.num_chunks == 0

    assert packet.header.flags.control is True
    assert packet.header.flags.resend is False
    assert packet.header.flags.compression is False
    assert packet.header.flags.connless is False

    assert packet.messages[0].message_name == 'close'
    assert len(packet.messages) == 1

def test_parse_7_close_fake_resend() -> None:
    packet: TwPacket = parse7(b'\x0c\x0a\x00\xaa\xbb\xcc\xdd\04') # 0.7 close
    #                   ^
    #                resending ctrl close
    #                probably never happens

    assert packet.version == '0.7'

    assert packet.header.ack == 10
    assert packet.header.token == b'\xaa\xbb\xcc\xdd'
    assert packet.header.num_chunks == 0

    assert packet.header.flags.control is True
    assert packet.header.flags.resend is True
    assert packet.header.flags.compression is False
    assert packet.header.flags.connless is False

    assert packet.messages[0].message_name == 'close'
    assert len(packet.messages) == 1

def test_parse_7_close_fake_num_chunks() -> None:
    packet: TwPacket = parse7(b'\x04\x0a\x01\xcf\xee\xde\x2d\04') # 0.7 close
    #                          ^
    #                       1 chunk makes no sense
    #                       because control messages should
    #                       always have 0 chunks

    assert packet.version == '0.7'

    assert packet.header.ack == 10
    assert packet.header.token == b'\xcf\xee\xde\x2d'
    assert packet.header.num_chunks == 1

    assert packet.header.flags.control is True
    assert packet.header.flags.resend is False
    assert packet.header.flags.compression is False
    assert packet.header.flags.connless is False

    assert packet.messages[0].message_name == 'close'
    assert len(packet.messages) == 1
