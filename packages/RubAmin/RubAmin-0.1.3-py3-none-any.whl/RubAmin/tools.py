from re import findall

class Tools(object):
	def __init__(self) -> int:
		...

	def textAnalysis(self , text : str) -> list:
		Results : list = []

		if not "@@" in text:
			realText : str = text.replace("**", "").replace("__", "").replace("``", "")
		else:
			realText: str = text.replace("@@", "").split(':')[0] if not text.replace("@@", "").split(':')[0].startswith('u') else text.replace("@@", "").split(':')[1]
			GUID: str = text.replace("@@", "").split(':')[1] if text.replace("@@", "").split(':')[1].startswith('u') else text.replace("@@", "").split(':')[0]

		bolds: list = findall(r"\*\*(.*?)\*\*" , text)
		italics: list = findall(r"\_\_(.*?)\_\_" , text)
		monos: list = findall(r"\`\`(.*?)\`\`" , text)
		if "@@" in text:
			text: str = text.split(':')[0] if not text.split(':')[0].startswith('u') else text.split(':')[1]
			mentions: list = findall(r"\@\@(.*?)\@\@" , text+'@@')

		bResult: list = [realText.index(i) for i in bolds]
		iResult: list = [realText.index(i) for i in italics]
		mResult: list = [realText.index(i) for i in monos]
		if '@@' in text:
			mentionsResult: list = [realText.index(i) for i in mentions]

		for bIndex , bWord in zip(bResult , bolds):
			Results.append({
				"from_index" : bIndex,
				"length" : len(bWord),
				"type" : "Bold"
			})

		for iIndex , iWord in zip(iResult , italics):
			Results.append({
				"from_index" : iIndex,
				"length" : len(iWord),
				"type" : "Italic"
			})

		for mIndex , mWord in zip(mResult , monos):
			Results.append({
				"from_index" : mIndex,
				"length" : len(mWord),
				"type" : "Mono"
			})

		if '@@' in text:
			for mentionIndex , mentionWord in zip(mentionsResult , mentions):
				Results.append({
					"from_index" : mentionIndex,
					"length" : len(mentionWord),
					"type" : "MentionText",
					"mention_text_object_guid": GUID,
					"mention_text_object_type": "User"
				})

		return Results , realText