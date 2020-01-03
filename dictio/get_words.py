import requests
import bs4

def parse_results(s):
	parsed = "".join(["<li>" + x + "</li>" for x in str(s).replace("</li>","").split("<li>")])
	parsed = bs4.BeautifulSoup(parsed, "html.parser")
	return [x.getText() for x in parsed.findAll("li")]

def get_word_defs(language, word):
	if language == "es":
		r = requests.get("https://www.wordreference.com/definicion/"+word)
	if language == "en":
		r = requests.get("https://www.wordreference.com/definition/"+word)
	s = bs4.BeautifulSoup(r.text,"html.parser")
	s = s.find(class_="entry")
	s = [x for x in parse_results(s) if x != ""]
	return {"word":word,"definitions":s}