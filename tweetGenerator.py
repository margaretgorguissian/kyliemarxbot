import json

class TweetGenerator:
	def __init__(self):
		self.rawTweets = None
		self.initialStates = None
		self.markovDictionary = None

	def loadTweets(self, fileName):
		self.rawTweets = self.loadJSON(fileName)

	def processTweets():
		pass

	def loadTweetGen(self, fileName):
		pass

	def saveTweetGen(self, fileName):
		pass

	def generateTweet():
		pass

	def loadJSON(self, fileName):
		with open(filename, 'r') as fileHandler:
			jsonData = json.load(fileHandler)
		return jsonData

	def saveJSON(self, jsonData, fileName)
		with open(fileName, 'w') as fileHandler
			json.dump(jsonData, fileHandler)
		print("JSON saved as {}.".format(fileName))