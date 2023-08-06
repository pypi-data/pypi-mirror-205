from .import connections
from json import loads , dumps
from .encryption import Encryption
from random import choice
from .createMethod import createMethod

class Rubino(object):
	def __init__(self , auth : str) -> int:
		self.auth : str = auth
		self.Method = createMethod(auth)
		self.post : str = connections.post
		self.url : str = 'https://rubino5.iranlms.ir/'# ,# 'https://rubino1.iranlms.ir/'

	async def getPostByShareLink(self , post_link : str , profile_id : str) -> dict:
		"""
			Attention
			In the profile_id argument, you must enter the profile ID of your user account !
		"""
		data : dict = {
			"share_string" : post_link.split('/')[-1] if '/' in post_link else post_link,
			"profile_id" : profile_id
		}
		data : str = await self.Method.createMethod( 0 , "getPostByShareLink" , data)
		return loads(await self.post(self.url , data))

	async def getExplore(self , profile_id : str) -> dict:
		"""
			Attention
			In the profile_id argument, you must enter the profile ID of your user account !
		"""
		data : dict = {
			"profile_id" : profile_id
		}
		data : str = await self.Method.createMethod( 0 , "getExplorePostTopics" , data)
		return loads(await self.post(self.url , data))