from setuptools import setup, find_packages

setup(
    name="asyncsocks5",
    version="0.1",  # Versione iniziale
    author="alegiacento",
    author_email="alexgiacento@gmail.com",
    description="Async request through SOCKS5 proxy",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlessandroGia/asyncsocks5.git",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
