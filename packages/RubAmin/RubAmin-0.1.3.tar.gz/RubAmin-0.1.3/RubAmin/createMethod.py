from .encryption import Encryption
from json import loads , dumps


class createMethod(object):
	'''
		This class is for creating and
		returning methods to send requests
		to the Rubik's server
	'''
	def __init__(self:str , auth:str) -> int:
		self.auth : str = auth
		self.enc : str = Encryption(auth)
		self.web : dict = {
			"app_name" : "Main",
			"app_version" : "4.2.0",
			"platform" : "Web",
			"package" : "web.rubika.ir",
			"lang_code" : "fa" } #   rubika web client
		self.android : dict = {
			"app_name" : "Main",
			"app_version" : "3.0.9",
			"platform" : "Android",
			"package" : "ir.resaneh1.iptv",
			"lang_code" : "fa"
		}
	
	async def createMethod(self , Type : int, Method : str , data : dict):
		'''
			This function is for
			creating data to send
			a request to the Rubika's server.
		'''
		if Type == 0:
			return dumps({
				"api_version" : "0",
				"auth" : self.auth,
				"client" : self.android,
				"data" : data,
				"method" : Method
			}).encode()

		elif Type == 4:
			data : str = dumps(
				{
					"api_version" : "4",
					"auth" : self.auth,
					"client" : self.android,
					"method" : Method,
					"data_enc" : self.enc.encrypt(dumps(data)
				)}).encode()
			return data

		elif Type == 5:
			return dumps(
				{"api_version" : "5",
				"auth" : self.auth,
				"data_enc" : self.enc.encrypt(
				dumps({
				"method" : Method,
				"input" : data,
				"client" : self.web
			}))}).encode()