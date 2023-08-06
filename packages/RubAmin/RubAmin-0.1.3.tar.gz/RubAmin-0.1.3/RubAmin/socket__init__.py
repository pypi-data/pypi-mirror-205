from websocket import create_connection
from json import dumps , loads
from random import choice
from .encryption import Encryption

class connect(object):
	def __init__(self , auth : str , displayWelcome : bool = True):
		if displayWelcome:
			...
		self.auth : str = auth
		self.wss : str = choice([
		'wss://jsocket2.iranlms.ir:80' ,
		'wss://msocket1.iranlms.ir:80' ,
		'wss://jsocket3.iranlms.ir:80'
		 ])

	async def connection(self) :
		ws = create_connection(self.wss)
		data : str = dumps({
			"api_version" : "5",
			"auth" : self.auth,
			"data_enc" : "",
			"method" : "handShake"
		})
		ws.send(data)
		while 1:
			try:
				yield loads(ws.recv())
			except : ...

class Client(object) :
	def __init__(self , auth : str) :
		self.auth : str = auth
		self.connect = connect(self.auth)
		self.enc = Encryption(self.auth)

	async def handler(self) :
		while 1:
			try:
				async for data in self.connect.connection():
					if data.get('type') == 'messenger':
						updates : dict = loads(self.enc.decrypt(data.get('data_enc'))).get('chat_updates')
						if not updates == None:
							yield updates
			except:
				...