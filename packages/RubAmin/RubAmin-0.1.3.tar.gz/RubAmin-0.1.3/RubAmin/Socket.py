from aiohttp import ClientSession
from random import choice
from json import dumps , loads
from .encryption import Encryption

class Socket(object):
	def __init__(self , auth : str) -> int:
		self.auth : str = auth
		self.wss : str = choice([
		'wss://jsocket2.iranlms.ir:80' ,
		'wss://msocket1.iranlms.ir:80' ,
		'wss://jsocket3.iranlms.ir:80'
		 ])
		self.enc = Encryption(self.auth)

	async def connection(self) -> dict:
		async with ClientSession() as session:
			async with session.ws_connect(self.wss) as ws:
				data : str = dumps({
					"api_version" : "5",
					"auth" : self.auth,
					"data_enc" : "",
					"method" : "handShake"
					})
				await ws.send_str(data)
				async for result in ws:
					result : dict = loads(result.data)
					if result.get('type') == 'messenger':
						try:
							yield loads(self.enc.decrypt(result.get('data_enc')))
						except :
							...