from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode , urlsafe_b64decode

class Encryption(object):
	def __init__(self , auth : str) -> int:
		self.key : str = bytearray(self.secret(auth), "UTF-8")
		self.iv : str = bytearray.fromhex('0' * 32)

	def replaceCharAt(self , e : str, t : str, i : str) -> str:
		return e[0:t] + i + e[t + len(i):]

	def secret(self , e : str):
		t : str = e[0:8]
		i : str = e[8:16]
		n : str = e[16:24] + t + e[24:32] + i
		s : int = 0
		while (s < len(n)):
			e : str = n[s]
			if e >= '0' and e <= '9':
				t : str = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
				n : str = self.replaceCharAt(n, s, t)
			else:
				t:str = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
				n : str = self.replaceCharAt(n, s, t)
			s += 1
		return n

	def encrypt(self , text : str) -> str:
		return b64encode(AES.new(self.key,
		AES.MODE_CBC, self.iv).encrypt(
		pad(text.encode('UTF-8'),
		AES.block_size))).decode('UTF-8')

	def decrypt(self , text : str) -> str:
		return unpad(AES.new(self.key,
		AES.MODE_CBC, self.iv).decrypt(
		urlsafe_b64decode(
		text.encode('UTF-8'))),
		AES.block_size).decode('UTF-8')