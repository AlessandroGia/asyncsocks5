from typing import Optional

class HTTPResponse:
    """
    A class to represent an HTTP response.

    :param raw_response: The raw response from the server.
    :type raw_response: str
    :param version: The HTTP version.
    :type version: str
    :param status: The status code.
    :type status: int
    :param reason: The reason phrase.
    :type reason: str
    :param headers: The response headers.
    :type headers: dict
    :param body: The response body.
    :type body: str
    """
    def __init__(self, raw_response: str):
        """
        Constructor for the HTTPResponse class.

        :param raw_response: The raw response from the server.
        :type raw_response: str
        """
        self.raw_response: str = raw_response
        self.version: str = ""
        self.status: int = 0
        self.reason: str = ""
        self.headers: dict = {}
        self.body: str = ""
        self.parse_response()

    def parse_response(self):
        """
        Parses the raw response from the server.

        :return:
        """
        parts = self.raw_response.split("\r\n\r\n", 1)
        header_section = parts[0]
        self.body = parts[1] if len(parts) > 1 else ""

        lines = header_section.split("\r\n")
        status_line = lines[0]  # Prima riga è la status line

        parts = status_line.split(" ", 2)
        self.version = parts[0]
        self.status = int(parts[1])
        self.reason = parts[2] if len(parts) > 2 else ""

        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                self.headers[key] = value

    def __repr__(self):
        return f"<HTTPResponse {self.status} {self.reason}>"

    def __str__(self):
        return f"HTTP Version: {self.version}\nStatus: {self.status} {self.reason}\nHeaders: {self.headers}\nBody: {self.body[:100]}..."

