import json
import re
from random import randint

class TweetGenerator:
	def __init__(self, sourceFile=None):
		self.rawTweets = []
		self.initialStates = []
		self.markovDictionary = {}
		if sourceFile:
			self.loadTweets(sourceFile)
			self.processTweets()
			self.saveTweetGen(sourceFile + "Markov")

	def loadTweets(self, fileName):
		self.rawTweets = self.loadJSON(fileName)

	def processTweets(self):
		endingChars = ["!", "?", ".", ","]

		priorWord = None
		for tweet in self.rawTweets:
			for word in tweet.split() + [None]:
				if priorWord is None and not word is None:
					self.initialStates.append(word)
					priorWord = word
				elif word is None:
					self.updateDictionary(priorWord, "END_OF_SENTENCE")
					priorWord = None
				elif word[-1] in endingChars:
					self.updateDictionary(priorWord, word)
					self.updateDictionary(word, "END_OF_SENTENCE")
					priorWord = None
				else:
					self.updateDictionary(priorWord, word)
					priorWord = word

	def updateDictionary(self, priorWord, word):
		if priorWord in self.markovDictionary:
			self.markovDictionary[priorWord].append(word)
		else:
			self.markovDictionary.update({priorWord:[word]})

	def loadTweetGen(self, fileName):
		allGenData = self.loadJSON(fileName)
		self.initialStates = allGenData['initialStates']
		self.markovDictionary = allGenData['markovDictionary']
		self.rawTweets = allGenData['rawTweets']
		print("{} Loaded".format(fileName))


	def saveTweetGen(self, fileName):
		allGenData = {'initialStates':self.initialStates, 
						'markovDictionary':self.markovDictionary,
						'rawTweets':self.rawTweets}
		self.saveJSON(allGenData, fileName)

	def generateTweet(self):
		word = self.initialStates[randint(0, len(self.initialStates) - 1)]
		tweet = [word]
		while word != "END_OF_SENTENCE":
			randomIndex = randint(0, len(self.markovDictionary[word]) - 1)
			word = self.markovDictionary[word][randomIndex]
			if not word == "END_OF_SENTENCE":
				tweet.append(word)
		return " ".join(tweet)

	def loadJSON(self, fileName):
		with open(fileName, 'r') as fileHandler:
			jsonData = json.load(fileHandler)
		return jsonData

	def saveJSON(self, jsonData, fileName):
		with open(fileName, 'w') as fileHandler:
			json.dump(jsonData, fileHandler)
		print("JSON saved as {}.".format(fileName))

	def loadTweetGen(self, fileName):
		allGenData = self.loadJSON(fileName)
		self.initialStates = allGenData['initialStates']
		self.markovDictionary = allGenData['markovDictionary']
		self.rawTweets = allGenData['rawTweets']
		print("{} Loaded".format(fileName))

	def saveTweetGen(self, fileName):
		allGenData = {'initialStates':self.initialStates, 
						'markovDictionary':self.markovDictionary,
						'rawTweets':self.rawTweets}
		self.saveJSON(allGenData, fileName)
##class MarxMaker:
##	def __init__(self, sourceFile=None):

class KylieTweetGenerator(TweetGenerator):
	def __init__(self, sourceFile=None):
		self.KJHashtags = []
		self.KJWords = ["lips", "Tyga", "lipkit", "realizing things", "snapchat"]
		## can I put this in a different class?
		self.MarxWords = ["communist", "struggle", "liberation", "proleteriat", "class struggles", "revolution", "bourgeoisie", "exploit", "labor", "opposition", "means of production","capitalism"]
		if sourceFile:
			TweetGenerator.__init__(self, sourceFile)
		else:
			TweetGenerator.__init__(self)

	def loadTweetGen(self, fileName):
		allGenData = self.loadJSON(fileName)
		self.initialStates = allGenData['initialStates']
		self.rawTweets = allGenData['rawTweets']
		self.markovDictionary = allGenData['markovDictionary']
		self.KJHashtags = allGenData['KJHashtags']
		print("{} Loaded".format(fileName))

	def saveTweetGen(self, fileName):
		allGenData = {'initialStates':self.initialStates,
						'rawTweets':self.rawTweets,
						'markovDictionary':self.markovDictionary,
						'KJHashtags':self.KJHashtags}
		self.saveJSON(allGenData, fileName)

	def collectHashtags(self):
		if self.rawTweets:
			hashtags = []
			hashtagRegex = r'#\w+[?.!,]?'
			for tweet in self.rawTweets:
				matches = re.findall(hashtagRegex, tweet)
				for match in matches:
					hashtags.append(match)
			self.KJHashtags = hashtags
		else:
			print("Please load Tweet Data Before Collecting Hashtags.")

	def removeLinks(self):
		if self.rawTweets:
			linkRegex = r'http:\w+[?!,]?'
			for tweet in self.rawTweets:
				re.sub(linkRegex, '', tweet)
		else:
			print("Please load Tweet Data Before Removing Links.")

	def loadTweets(self, fileName):
		TweetGenerator.loadTweets(self, fileName)
		self.collectHashtags()
		self.removeLinks()

	def generateKylieTweet(self):
		finalTweet = []
		while finalTweet == [] or len(finalTweet) > 144 or len(finalTweet) < 35:
			finalTweet =[]
			for _ in range (randint(1, 3)):
				finalTweet.append(self.generateTweet())
			## this can be done so much better
			if randint(0, 1):
				finalTweet.append(self.KJWords[randint(0, len(self.MarxWords) - 1)])
			if randint(0, 1):
				finalTweet.append(self.MarxWords[randint(0, len(self.KJWords) - 1)])
			if randint(0, 1):
				finalTweet.append(self.KJHashtags[randint(0, len(self.KJHashtags) - 1)])
			finalTweet = " ".join(finalTweet)
		return finalTweet
