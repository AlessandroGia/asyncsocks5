from asyncio import open_connection, StreamReader, StreamWriter
from contextlib import asynccontextmanager

from asyncsocks5.parser import HTTPResponse
from asyncsocks5.rfc1928 import ReplyCodes

import struct

class AsyncProxySocks:

    def __init__(self, server_ip: str, server_port: int, username: str = None, password: str = None):
        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__username = username
        self.__password = password

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    async def __fetch_http(reader: StreamReader, writer: StreamWriter, url: str) -> HTTPResponse:
        writer.write(f"GET / HTTP/1.1\r\nHost: {url}\r\nConnection: close\r\n\r\n".encode())
        await writer.drain()

        response = bytearray()
        while chunk := await reader.read(4096):
            response.extend(chunk)

        return HTTPResponse(response.decode())

    @staticmethod
    async def __auth_no_credentials(reader: StreamReader, writer: StreamWriter) -> bytes:
        req = b"\x05\x01\x00"
        writer.write(req)
        await writer.drain()

        return await reader.read(2)

    @staticmethod
    async def __auth_with_credentials(reader: StreamReader, writer: StreamWriter, username: str, password: str) -> bytes:
        req = b"\x05\x01\x02"
        writer.write(req)
        await writer.drain()

        auth_request = struct.pack("!B", 0x01) + struct.pack("!B", len(username)) + username.encode() + struct.pack("!B", len(password)) + password.encode()
        writer.write(auth_request)
        await writer.drain()

        return await reader.read(2)

    @staticmethod
    async def __connect_to_server(reader: StreamReader, writer: StreamWriter, url: str, port: int) -> None:
        request = b"\x05\x01\x00\x03" + bytes([len(url)]) + url.encode() + struct.pack("!H", port)
        writer.write(request)
        await writer.drain()

        response = await reader.read(2)
        if response[1] != 0x00:
            raise Exception(ReplyCodes.from_code(response[1]).description)

    async def __sub_negotiation(self, reader: StreamReader, writer: StreamWriter) -> None:

        if self.__username and self.__password:
            response = await self.__auth_with_credentials(reader, writer, self.__username, self.__password)
        else:
            response = await self.__auth_no_credentials(reader, writer)

        if response[1] != 0x00:
            raise Exception(ReplyCodes.from_code(response[1]).description)

    @asynccontextmanager
    async def get(self, url: str, port: int = 80) -> HTTPResponse:
        url = url.removeprefix("http://").rstrip("/")
        writer = None
        try:
            reader, writer = await open_connection(self.__server_ip, self.__server_port)
            await self.__sub_negotiation(reader, writer)
            await self.__connect_to_server(reader, writer, url, port)
            yield await self.__fetch_http(reader, writer, url)
        finally:
            if writer:
                writer.close()
                await writer.wait_closed()
