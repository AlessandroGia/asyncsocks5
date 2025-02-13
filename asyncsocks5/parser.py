
class HTTPResponse:
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.version = None
        self.status = None
        self.reason = None
        self.headers = {}
        self.body = None
        self.parse_response()

    def parse_response(self):
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

