from PIL import Image
from base64 import b64encode
from io import BytesIO

class media(object):
	def __init__(self) -> int:
		...

	async def getImageThumbnail(self , image_bytes : bytes) -> bytes:
		im = Image.open(BytesIO(image_bytes))
		[width , height] = im.size
		if height > width:
			new_height : int = 40
			new_width  = round(new_height * width / height)
		else:
			new_width : int = 40
			new_height : int = round(new_width * height / width)
			im = im.resize((new_width , new_height), Image.ANTIALIAS)
			changed_image : bytes = BytesIO()
			im.save(changed_image , format='PNG')
			changed_image : bytes = changed_image.getvalue()
		return b64encode(changed_image)

	def getImageSize(self , image_bytes : bytes) -> tuple:
		im = Image.open(BytesIO(image_bytes))
		[width , height] = im.size
		return [width , height]