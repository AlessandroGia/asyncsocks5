# AsyncProxySocks

Library to connect to a SOCKS5 proxy server asynchronously.

## Requirements
- Python 3.8 or higher
- Build 
```pip
pip install build
```

## Build
```sh
python -m build --wheel
```

## Installation
```sh
cd dist
pip install *.whl
```

## Usage
```python
import asyncio
from asyncsocks5.proxy import AsyncProxySocks

async def main():
    async with AsyncProxySocks("proxy_ip", 1080, "user", "pass") as proxy:
        async with proxy.get("http://example.com") as response:
            ...

asyncio.run(main())
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


