import json
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('This is a log message.')
import re
from random import randint

# TweetGenerator makes a Markov dictionary of all of Kylie Jenner's tweets
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
		self.removeLinks()
		self.removeTwitterTags()   
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

	def removeLinks(self):
		if self.rawTweets:
			linkRegex = r'https\w+[?!,]?'
			for tweet in self.rawTweets:
				re.sub(linkRegex, '', tweet)
		else:
			print("Please load Tweet Data Before Removing Links.")

	def removeTwitterTags(self):
		if self.rawTweets:
			tagRegex = r'@\w+[?.!,]?'
			for tweet in self.rawTweets:
				re.sub(tagRegex, '', tweet)
		else:
			print("Please load Tweet Data Before Removing Links.")

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

# MarxMaker adds Marx text to the priorMarkov dictionary
class MarxMaker:
	def __init__(self, sourceFile=None):
		self.rawText = []
		self.initialStates = []
		if sourceFile:
			self.loadText(sourceFile)
			self.processText()
			self.saveTextGen(sourceFile + "Markov")

	def loadText(self, fileName):
		print("Loading Marx JSON ...")
		print(fileName)
		with open(fileName, 'r') as fileHandler:
			print("in File")
			self.rawText = json.load(fileHandler)
		print("Marx JSON loaded.")

	def processText(self):
		endingChars = ["!", "?", ".", ",", "\n"]
		priorWord = None
		for line in self.rawText:
			for word in line.split() + [None]:
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

	def loadTextGen(self, fileName):
		allGenData = self.loadJSON(fileName)
		self.initialStates = allGenData['initialStates']
		self.markovDictionary = allGenData['markovDictionary']
		self.rawText = allGenData['rawText']
		print("{} Loaded".format(fileName))

	def saveTextGen(self, fileName):
		allGenData = {'initialStates':self.initialStates, 
						'markovDictionary':self.markovDictionary,
						'rawText':self.rawText}
		self.saveJSON(allGenData, fileName)

	def saveJSON(self, jsonData, fileName):
		with open(fileName, 'w') as fileHandler:
			json.dump(jsonData, fileHandler)
		print("JSON saved as {}.".format(fileName))


class KylieTweetGenerator(TweetGenerator, MarxMaker):
	def __init__(self, sourceFile=None, marxFile="MarxDump"):
		self.KJHashtags = []
		self.KJWords = ["lips", "Tyga", "lipkit", "realizing things", "snapchat"]
		if sourceFile:
			print("sourceFile exists")
			TweetGenerator.__init__(self, sourceFile)
			if marxFile:
				print("marxFile exists")
				MarxMaker.__init__(self, marxFile)
			print("TweetGenerator initialized.")
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

	def loadTweets(self, fileName):
		TweetGenerator.loadTweets(self, fileName)
		self.collectHashtags()

	def generateKylieTweet(self):
		finalTweet = []
		while finalTweet == [] or len(finalTweet) > 144 or len(finalTweet) < 35:
			finalTweet =[]
			for _ in range (randint(1, 3)):
				finalTweet.append(self.generateTweet())
			if randint(0, 1):
				finalTweet.append(self.KJHashtags[randint(0, len(self.KJHashtags) - 1)])
			finalTweet = " ".join(finalTweet)
		return finalTweet
