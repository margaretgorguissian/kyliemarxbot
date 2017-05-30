# @KylieMarxBot  
A twitter bot that concatenates tweets from Kylie Jenner with excerpts from Karl Marx's collected works  
**Author Name:** Margaret Gorguissian  
**Date:** 03/25/2017
***  
This project made heavy use of the [Make America Tweet Again](http://joedevelops.com/2016/07/30/make-america-tweet-again-part-1/) tutorial
from JoeDevelops. This is a fun project in order to teach myself elements of
Python and to familiarize myself with aspects of the Twitter API. Through this
project, I also learned about text generation and data storage methods.  
  
### Purpose  
The purpose of this project is to combine the tweets of Kylie Jenner with the 
texts of Karl Marx, and to have those combinations be tweeted automatically 
from a special twitter account with the handle @KylieMarxBot.  

### Method
* Tweets from @KylieJenner were accessed through Tweepy

### Issues
* Having issue reading Marx Dump, even after separating sentences. Program quits when it comes time to read the Marx file
    * From troubleshooting and research, I believe it's because my Marx JSON file is too big for the JSON reader to handle. The Marx JSON file is 80kb, while the Kylie Jenner JSON file is only 5kb. I am trying with a much smaller Marx file, and will update from there. (5/24/2017)
    * I shortened the Marx Dump significantly, and the Kylie Marx tweet generation was successful. (5/30/2017)
* By adding Marx text and Kylie tweets to the same Markov dictionary, the Kylie Marx tweets are largely non-sensical. (When it is just generating a Kylie Jenner tweet using the Markov dictionary, it performs much better). There is probably a better method of generating Kylie Marx tweets than just using a single Markov dictionary.
    * I am contemplating generating half the tweet using a Kylie Jenner Markov dictionary, and the other half of the tweet using a Karl Marx Markov dictionary, and then combining the two. (5/30/2017)


### Resources/References/Inspiration  
* [Make America Tweet Again](http://joedevelops.com/2016/07/30/make-america-tweet-again-part-1/)
* [Generating pseudo random text with Markov chains using Python](http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/)
* [Generating a random string](https://pythontips.com/2013/07/28/generating-a-random-string/)
* [Chomsky random text generator](http://code.activestate.com/recipes/440546-chomsky-random-text-generator/)
* [Parsing JSON in Python](https://temboo.com/python/parsing-json)
* [Karl Marx in Project Gutenberg](http://www.gutenberg.org/ebooks/author/46)
