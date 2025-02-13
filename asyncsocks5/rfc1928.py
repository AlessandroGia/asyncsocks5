from enum import Enum


class ReplyCodes(Enum):
    SUCCEEDED = (0x00, "succeeded")
    GENERAL_FAILURE = (0x01, "general failure")
    CONNECTION_NOT_ALLOWED = (0x02, "connection not allowed")
    NETWORK_UNREACHABLE = (0x03, "network unreachable")
    HOST_UNREACHABLE = (0x04, "host unreachable")
    CONNECTION_REFUSED = (0x05, "connection refused")
    TTL_EXPIRED = (0x06, "TTL expired")
    COMMAND_NOT_SUPPORTED = (0x07, "command not supported")
    ADDRESS_TYPE_NOT_SUPPORTED = (0x08, "address type not supported")
    UNASSIGNED = (0x09, "unassigned")

    def __init__(self, code, description):
        self.code = code
        self.description = description

    @classmethod
    def from_code(cls, code):
        for reply in cls:
            if reply.code == code:
                return reply
        return cls.UNASSIGNED