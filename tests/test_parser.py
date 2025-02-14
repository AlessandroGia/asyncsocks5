from asyncsocks5.parser import HTTPResponse

def test_http_response():
    raw_response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 10\r\n\r\nHello World"
    response = HTTPResponse(raw_response)
    assert response.version == "HTTP/1.1"
    assert response.status == 200
    assert response.reason == "OK"
    assert response.headers == {"Content-Type": "text/html", "Content-Length": "10"}
    assert response.body == "Hello World"