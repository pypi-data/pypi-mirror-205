from setuptools import setup

requirements : list = ["pycryptodome" , "pillow" , "aiohttp" , "websocket-client"]

setup(
    name = "RubAmin",
    version = "0.1.3",
    author = "Amin Tatality",
    description = "t.me/M_AminB78",
    long_description = "t.me/M_AminB78\nInstagram.com\m_aminb78",
    long_description_content_type ="text/markdown",
    packages = ['RubAmin'],
    install_requires = requirements,
    classifiers = [],
)