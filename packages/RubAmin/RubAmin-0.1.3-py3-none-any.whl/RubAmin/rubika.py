from time import sleep , time
from .encryption import Encryption
from .import connections
from json import dumps , loads
from random import randint , choice
from .createMethod import createMethod
from .tools import Tools

__version__ : str = '0.1.3'
__author__ : str = 'Amin Tatality'

class Rubika(object):
	def __init__(self , auth : str , displayWelcome : bool = True) -> int:
		if displayWelcome: 
			text : str = f'This library was created by {__author__}, with versions {__version__} ...\n\n'
			for char in text:
				print(char , flush = True , end = '')
				sleep(.01)
		self.auth : str = auth # account auth for connect to rubika server
		self.post : str = connections.post
		self.enc : str = Encryption(self.auth)
		self.Method : int = createMethod(self.auth)
		self.url : str = choice([
			'https://messengerg2c26.iranlms.ir' ,
			'https://messengerg2c46.iranlms.ir' ,
			'https://messengerg2c39.iranlms.ir'
			])
		self.Tool = Tools()
		self.uploaderFile = connections.upload
	
	async def getChatsUpdate(self) -> dict:
		'''This function is for
		receiving the latest messages
		that have been sent to your account...'''
		data : str = await self.Method.createMethod(
		5 ,
		'getChatsUpdates', 
		{
			"state" : str(round(time() - 200))
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data').get('chats')

	async def getChats(self , start_id : bool = None) -> dict:
		data : str = await self.Method.createMethod(
		5 ,
		"getChats" , 
		{
			"start_id" : start_id
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data')

	async def getUserInfo(self , user_guid : str) -> dict:
		data : str = await self.Method.createMethod(
		5 ,
		"getUserInfo" , 
		{
			"user_guid" : user_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data')

	async def getLinkFromAppUrl(self , url : str) -> dict:
		data : str = await self.Method.createMethod(
		5 ,
		"joinChannelAction" , 
		{
			"action" : "Join",
			"channel_guid" : "c0i93V0298ff8aa1b8c5cf0bcb72d2d1"
		})
		while 1:
			try:
				loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))
				break
			except:
				continue
		data : str = await self.Method.createMethod(
		5 ,
		"getLinkFromAppUrl" , 
		{
			"app_url" : url
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data').get('link').get('open_chat_data')

	async def getBannedGroupMembers(self , group_guid : str) -> dict:
		"""
			You can get group banned users...
		"""
		data : str = await self.Method.createMethod(
		5 ,
		"getBannedGroupMembers" , 
		{
			"group_guid" : group_guid
		},
		"android"
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data')

	async def getGroupAdmins(self , group_guid : str) -> dict:
		'''
			You can get the admins of a group with the group ID, just enter the group ID that starts with g in the first argument and your robot account must be in the admin group.
		'''
		data : str = await self.Method.createMethod(
		5 ,
		'getGroupAdminMembers' , 
		{
			"group_guid" : group_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data').get('in_chat_members')

	async def sendMessage(self : str , chat_id : str , text : str , metaData = None , replying_message_id : bool = None) -> dict:
		'''Using this function, you can send
		a text message to the desired
		chat, in the first argument,
		you must enter the chat ID where
		the message is to be sent (GUID)
		and in the second argument,
		enter your message as a string
		in the last argument.
		That is, thirdly, if you are going
		to reply to the message,
		click on the message ID,
		the message that is going
		to be replied to (not required).'''
		Input : dict = {
			"object_guid" : chat_id,
			"rnd" : f"{randint(100000,999999999)}",
			"text" : text,
			"reply_to_message_id" : replying_message_id
		}
		if metaData != None:
			Input['metadata'] = {'meta_data_parts' : metaData}
		mode : list = ['**' , '__' , '``', '@@']
		for check in mode:
			if check in text:
				metadata : list = self.Tool.textAnalysis(text)
				Input['metadata'] = {'meta_data_parts' : metadata[0]}
				Input['text'] = metadata[1]
		data : dict = await self.Method.createMethod(5 , "sendMessage", Input)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def deleteMessages(self , chat_id : str , messages_id : list) -> dict:
		'''
			This function is delete message from chat
		'''
		data : str = await self.Method.createMethod(
		5 ,
		"deleteMessages",
		{
			"object_guid" : chat_id,
			"message_ids" : messages_id,
			"type" : "Global"
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data').get('chats')

	async def sendGroupVoiceChatActivity(self , group_guid : str , voice_chat_id : str) -> dict:
		'''
			This function is send Group Voice Chat
			Activity for send Voice
		'''
		data : str = await self.Method.createMethod(
		5 ,
		'sendGroupVoiceChatActivity' , 
		{
			"activity" : "Speaking",
			"chat_guid" : group_guid,
			"voice_chat_id" : voice_chat_id,
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getGroupVoiceChatUpdates(self , group_guid : str , voice_chat_id : str) -> dict:
		'''
			Get Group Voice Chat Updates with group guid and voice chat id
			you can write your group guid in the one arg
			you can write your voice chat id in the two arg
		'''
		data : str = await self.Method.createMethod(
		5 ,
		"getGroupVoiceChatUpdates" , 
		{
			"state" : randint(1000000000 , 9999999999),
			"chat_guid" : group_guid,
			"voice_chat_id" : voice_chat_id,
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data')

	async def requestSendFile(self , file_name : str , size : str , mime : str):
		"""
			This method is used when
			you want to upload a file
			to the Rubika's server
		"""
		Trying : int = 0
		while Trying != 5:
			try:
				data : str = await self.Method.createMethod(
				5 ,
				"requestSendFile" , 
				{
					"file_name" : file_name,
					"size" : size,
					"mime" : mime,
				})
				return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data')
			except :
				Trying += 1

	async def uploadFile(self , url : str , access_hash_send : str , file_id : str , byte : bytes):		
		"""
			This method is used to upload
			any type of file in Rubika
			server, this is a main method
			for uploads.
		"""
		if len(byte) <= 131072:
			header : dict = {
				"access-hash-send" : access_hash_send,
				"file-id" : file_id,
				"part-number" : "1",
				"total-part" : "1",
				"chunk-size" : str(len(byte)),
				"auth" : self.auth
			}
			result = loads(await self.uploaderFile(
			url,
			byte,
			header
			))
			return result.get('data').get('access_hash_rec')
		else:
			total_part : int = len(byte) / 131072 

	async def sendImage(self , chat_id : str , file_id : str , mime : str , dc_id : str , access_hash_rec : str , file_name : str , size : str , thumbnail : bytes , width : str , height : str , caption : bool = None , message_id : bool = None) -> dict:
		"""
			you can send photo in the a chat
		"""
		Input : dict = {
			"object_guid" : chat_id,
			"rnd" : f"{randint(100000 , 999999)}",
			"text" : caption,
			"reply_to_message_id" : message_id,
			"file_inline" : {
				"access_hash_rec" : str(access_hash_rec),
				"dc_id" : str(dc_id),
				"file_id" : str(file_id),
				"file_name" : file_name,
				"mime" : mime,
				"size" : size,
				"width" : width,
				"height" : height,
				"thumb_inline" : thumbnail,
				"type" : "Image"
		}}
		mode : list = ['**' , '__' , '``']
		for check in mode:
			if check in caption:
				metadata : list = self.Tool.textAnalysis(caption)
				Input['metadata'] = {'meta_data_parts' : metadata[0]}
				Input['text'] = metadata[1]
		data : dict = await self.Method.createMethod(5 , 'sendMessage', Input)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def sendFile(self , chat_id : str , access_hash_rec : str , dc_id : str , file_id : str , file_name : str , mime : str , size : str , caption : bool = None , replying_message_id : bool = None) -> dict:
		"""
			This is the main method for
			sending files with mp3, mp4,
			zip, etc. extensions, it can be
			said that it is an
			attachment/documemt sending method!
		"""
		if caption == None:
			if replying_message_id == None:
				t = 0
				while t < 3:
					try:
						Input : dict = {
							"object_guid" : chat_id,
							"rnd" : f"{randint(100000 , 999999)}",
							"file_inline" : {
								"access_hash_rec" : str(access_hash_rec),
								"dc_id" : str(dc_id),
								"file_id" : str(file_id),
								"file_name" : file_name,
								"mime" : mime,
								"size" : size,
								"type" : "File"
						}}
						data : dict = await self.Method.createMethod(5 , 'sendMessage', Input)
						return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))
						t+=3
					except: t+=1
			else:
				t = 0
				while t < 3:
					try:
						Input : dict = {
							"object_guid" : chat_id,
							"rnd" : f"{randint(100000 , 999999)}",
							"reply_to_message_id" : replying_message_id,
							"file_inline" : {
								"access_hash_rec" : str(access_hash_rec),
								"dc_id" : str(dc_id),
								"file_id" : str(file_id),
								"file_name" : file_name,
								"mime" : mime,
								"size" : size,
								"type" : "File"
						}}
						data : dict = await self.Method.createMethod(5 , 'sendMessage', Input)
						return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))
						t+=3
					except: t+=1

		else:
			if replying_message_id == None:
				t = 0
				while t < 3:
					try:
						Input : dict = {
							"object_guid" : chat_id,
							"rnd" : f"{randint(100000 , 999999)}",
							"text" : caption,
							"file_inline" : {
								"access_hash_rec" : str(access_hash_rec),
								"dc_id" : str(dc_id),
								"file_id" : str(file_id),
								"file_name" : file_name,
								"mime" : mime,
								"size" : size,
								"type" : "File"
						}}
						mode : list = ['**' , '__' , '``']
						for check in mode:
							if check in caption:
								metadata : list = self.Tool.textAnalysis(caption)
								Input['metadata'] = {'meta_data_parts' : metadata[0]}
								Input['text'] = metadata[1]
						data : dict = await self.Method.createMethod(5 , 'sendMessage', Input)
						return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))
						t+=3
					except: t+=1
			else:
				t = 0
				while t < 3:
					try:
						Input : dict = {
							"object_guid" : chat_id,
							"rnd" : f"{randint(100000 , 999999)}",
							"text" : caption,
							"reply_to_message_id" : replying_message_id,
							"file_inline" : {
								"access_hash_rec" : str(access_hash_rec),
								"dc_id" : str(dc_id),
								"file_id" : str(file_id),
								"file_name" : file_name,
								"mime" : mime,
								"size" : size,
								"type" : "File"
						}}
						mode : list = ['**' , '__' , '``']
						for check in mode:
							if check in caption:
								metadata : list = self.Tool.textAnalysis(caption)
								Input['metadata'] = {'meta_data_parts' : metadata[0]}
								Input['text'] = metadata[1]
						data : dict = await self.Method.createMethod(5 , 'sendMessage', Input)
						return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))
						t+=3
					except: t+=1

	async def editMessage(self , chat_id : str , message_id : str , text : str , metaData = None) -> dict:
		'''This method is for editing messages and working with this method is very simple; Enter the chat ID in the first argument, the message ID in the second argument, and the new text in the third argument...'''
		Input : dict = {
			"message_id" : message_id,
			"object_guid" : chat_id,
			"text" : text,
		}
		mode : list = ['**' , '__' , '``']
		for check in mode:
			if check in text:
				metadata : list = self.Tool.textAnalysis(text)
				Input['metadata'] = {'meta_data_parts' : metadata[0]}
				Input['text'] = metadata[1]
		if metaData != None:
			Input['metadata'] = {'meta_data_parts' : metaData}
		data : dict = await self.Method.createMethod(5 , 'editMessage', Input)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def banGroupMember(self : str , group_guid : str , user_guid : str ,) -> dict:
		'''You can remove a person
		from your group by using
		this function, just enter the
		group ID (GUID) in the first
		argument and the user ID in
		the second argument.'''
		# bot.banGroupMember('Group Guid' , 'User Guid')
		data : str = await self.Method.createMethod(
			5 ,
			'banGroupMember', 
			{
			'action' : 'Set',
			'group_guid' : group_guid,
			'member_guid' : user_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def searchInChannelMembers(self , channel_guid : str , search_text : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			'getChannelAllMembers', 
			{
			'channel_guid' : channel_guid,
			'search_text' : search_text
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getChannelAllMembers(self , channel_guid : str) -> bool:
		data : str = await self.Method.createMethod(
			5 ,
			'getChannelAllMembers', 
			{
				'channel_guid' : channel_guid,
				'search_text' : None,
				"start_id" : None
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def checkMemberInChannel(self , channel_guid : str , search_text : str , member_id : str) -> bool:
		data : str = await self.Method.createMethod(
			5 ,
			'getChannelAllMembers', 
			{
			'channel_guid' : channel_guid,
			'search_text' : search_text
		})
		get_data : dict = loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data').get('in_chat_members')
		for check in get_data:
			if check['username'] != '':
				if check['username'] == member_id:
					return True
			else:
				return 'No UserName!'
		return False

	async def getMessagesUpdates(self , chat_id : str) -> dict:
		data : str = await self.Method.createMethod(
		5 ,
		"getMessagesUpdates",
		{
			"object_guid" : chat_id,
			"state" : str(round(time() - 200))
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def forwardMessages(self , from_guid : str , messages_id : list , to_guid : str) -> dict:
		data : str = await self.Method.createMethod(
		5 ,
		"forwardMessages",
		{
			"from_object_guid" : from_guid,
			"message_ids": messages_id,
			"rnd": f"{randint(100000,999999999)}",
			"to_object_guid": to_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getGroupInfo(self , group_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getGroupInfo", 
			{
			'group_guid' : group_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data')

	async def getGroupLastMessageId(self , group_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getGroupInfo", 
			{
			'group_guid' : group_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data').get('chat').get('last_message_id')

	async def getChannelLastMessageId(self , channel_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getChannelInfo", 
			{
			'channel_guid' : channel_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data').get('chat').get('last_message_id')

	async def getChannelInfo(self, channel_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getChannelInfo", 
			{
			'channel_guid' : channel_guid,
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get('data').get('channel')

	async def getMessagesInterval(self , chat_id : str , middle_message_id : str) -> dict:
		return loads(self.enc.decrypt(loads(await self.post(
		self.url ,
		await self.Method.createMethod(
			5 
			, 'getMessagesInterval', 
			{
			'object_guid' : chat_id,
			'middle_message_id' : middle_message_id
			})
		)).get('data_enc'))).get('data').get('messages')

	async def getInfoByUsername(self , username : str) -> dict:
		'''
			You can get the information of a user with that user's ID
		'''
		return loads(self.enc.decrypt(loads(await self.post(
		self.url ,
		await self.Method.createMethod(
			5 ,
			"getObjectByUsername" , 
			{
				"username" : username.replace('@' , '') if '@' in username else username
			})
		)).get('data_enc'))).get('data')

	async def unBanGroupMember(self , group_guid : str , user_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			'banGroupMember', 
			{
			'action' : 'Unset',
			'group_guid' : group_guid,
			'member_guid' : user_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getGroupLink(self , group_guid : str) -> str:
		'''
			you can get your group link with this method
		'''
		data : str = await self.Method.createMethod(
			5 ,
			"getGroupLink", 
			{
			'group_guid' : group_guid,
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get("data").get("join_link")

	async def addGroupMembers(self , group_guid : str , member_guids : list) -> dict:
		'''
			With this method, you can add people to your group with their IDs that start with u, only your group should not be limited and that you give the user IDs as a list to the argument.
		'''
		data : str = await self.Method.createMethod(
			5 ,
			"addGroupMembers", 
			{
			"member_guids" : member_guids,
			"group_guid": group_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get("data")

	async def addChannelMembers(self , channel_guid : str , member_guids : list) -> dict:
		'''
			With this method, you can add people to your channel with their IDs that start with u, only your channel should not be limited and that you give the user IDs as a list to the argument.
		'''
		data : str = await self.Method.createMethod(
			5 ,
			"addChannelMembers", 
			{
			"member_guids" : member_guids,
			"channel_guid" : channel_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get("data")

	async def getMessagesInfo(self , chat_id : str , message_ids : list) -> dict:
		'''
			You can get the message information using their IDs, which are so-called numbers. You must give the message IDs as a list to the argument.
			[ '8392982728' ]
		'''
		data : str = await self.Method.createMethod(
			5 ,
			"getMessagesByID", 
			{
				"object_guid" : chat_id,
				"message_ids" : message_ids
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc'))).get("data")

	async def setMembersAccess(self , group_guid : str , access : list) -> dict:
		data : str = await self.Method.createMethod(
			4 ,
			"setGroupDefaultAccess", 
			{
				"access_list": access,
				"group_guid": group_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getGroupMembers(self , group_guid : str , start_id : bool = None) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getGroupAllMembers", 
			{
				"start_id" : start_id,
				"group_guid" : group_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def setGroupLink(self , group_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"setGroupLink", 
			{
				"group_guid" : group_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def setGroupTimer(self , group_guid : str , Time : str) -> dict:
		data : str = await self.Method.createMethod(
			4 ,
			"editGroupInfo", 
			{
				"group_guid" : group_guid,
				"slow_mode" : Time,
				"updated_parameters" : ["slow_mode"]
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def setGroupAdmin(self , group_guid : str , user_guid : str , access : list) -> dict:
		data : str = await self.Method.createMethod(
			4 ,
			"setGroupAdmin", 
			{
				"group_guid" : group_guid,
				"access_list" : access,
				"action" : "SetAdmin",
				"member_guid" : user_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def deleteGroupAdmin(self , group_guid : str , user_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			4 ,
			"setGroupAdmin", 
			{
				"group_guid" : group_guid,
				"action" : "UnsetAdmin",
				"member_guid" : user_guid
		})
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def logout(self) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"logout", 
			{}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def seenChats(self , seen_list : list) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"seenChats", 
			{
				"seen_list" : seen_list
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def sendChatActivity(self , chat_id : str , action : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"sendChatActivity", 
			{
				"activity" : action,
				"object_guid" : chat_id
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def pinMessage(self , chat_id : str , message_id : str) -> dict:
		data : str = await self.Method.createMethod(
			4 ,
			"setPinMessage", 
			{
				"action" : "Pin",
				"message_id" : message_id,
				"object_guid" : chat_id
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def unPinMessage(self , chat_id : str , message_id : str) -> dict:
		data : str = await self.Method.createMethod(
			4 ,
			"setPinMessage", 
			{
				"action" : "Unpin",
				"message_id" : message_id,
				"object_guid" : chat_id
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def joinGroup(self , group_link : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"joinGroup", 
			{
				"hash_link" : group_link.split('/')[-1]
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def groupPreviewByJoinLink(self , group_link : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"groupPreviewByJoinLink", 
			{
				"hash_link" : group_link.split('/')[-1]
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def leaveGroup(self , group_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"leaveGroup", 
			{
				"group_guid" : group_guid
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getGroupMentionList(self , group_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getGroupMentionList", 
			{
				"group_guid" : group_guid
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def block(self , user_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"setBlockUser", 
			{
				"action" : "Block",
				"user_guid" : user_guid
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def unBlock(self , user_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"setBlockUser", 
			{
				"action" : "Unblock",
				"user_guid" : user_guid
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getMyStickerSets(self) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getMyStickerSets", 
			{}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def createGroupVoiceChat(self , chat_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"createGroupVoiceChat", 
			{
				"chat_guid" : chat_guid
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def discardGroupVoiceChat(self , chat_guid : str , voice_chat_id : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"discardGroupVoiceChat", 
			{
				"chat_guid" : chat_guid,
				"voice_chat_id" : voice_chat_id
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getChannelLink(self , channel_guid : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getChannelLink", 
			{
				"channel_guid" : channel_guid,
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getAvatars(self , chat_id : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getAvatars", 
			{
				"object_guid" : chat_id,
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def deleteAvatar(self , chat_id : str , avatar_id : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"deleteAvatar", 
			{
				"object_guid" : chat_id,
				"avatar_id" : avatar_id
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def deleteChatHistory(self , chat_guid : str , last_message_id : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"deleteChatHistory", 
			{
				"object_guid" : chat_guid,
				"last_message_id" : str(last_message_id)
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def searchGlobalObjects(self , searchText : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"searchGlobalObjects", 
			{
				"search_text" : searchText
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

	async def getPollStatus(self , poll_id : str) -> dict:
		data : str = await self.Method.createMethod(
			5 ,
			"getPollStatus", 
			{
				"poll" : str(poll_id)
			}
		)
		return loads(self.enc.decrypt(loads(await self.post(self.url , data)).get('data_enc')))

class client(object):
	def __init__(self : int , auth : str) -> int:
		try:
			open('answered.txt', 'r').read()
		except FileNotFoundError:
			open('answered.txt', 'w').write('created By Shtyhon :)')
	
		self.auth : str = auth
		self.bot : str = Rubika(self.auth)
	
	async def chats(self : str) -> dict:
		'''
			This function in the client class , is
			a handler to receive the
			latest messages using
			the getChatsUpdate method.
		'''
		while 1:
			try:
				chats : str = await self.bot.getChatsUpdate()
				for chat in chats:
					if not chat['object_guid']+chat['last_message']['message_id'] in open('answered.txt', 'r').read().split('\n'):
						yield chat
						open('answered.txt','a+').write('\n'+chat['object_guid']+chat['last_message']['message_id'])
			except :
				...