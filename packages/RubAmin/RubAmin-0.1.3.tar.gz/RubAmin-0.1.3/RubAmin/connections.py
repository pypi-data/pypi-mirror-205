from aiohttp import ClientSession
from json import dumps , loads

async def get(url: str) -> dict:
	async with ClientSession() as session:
		async with session.get(url) as _:
			return _.text()

async def post(url: str , data: dict) -> dict:
	async with ClientSession() as _:
		async with _.post(url, data=data) as Post:
			return await Post.text()

async def upload(url : str , data : bytes , header) -> dict:
	async with ClientSession() as _:
		async with _.post(url, data=data , headers = header) as Post:
			return await Post.text()