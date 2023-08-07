from typing import Protocol

class CtrlMessage(Protocol):
    message_name: str
    message_id: int
    def unpack(self, data: bytes, we_are_a_client: bool = True) -> bool:
        ...
    def pack(self, we_are_a_client: bool = True) -> bytes:
        ...
