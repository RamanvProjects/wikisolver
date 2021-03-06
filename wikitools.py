#!/usr/bin/env python

import urllib
import json
import time

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class WikiSolver:
	"""A number of functions to be used with Wikipedia and its API"""
	def __init__(self, linkInit, linkFinal):
		self.linkInit = linkInit
		self.linkFinal = linkFinal
		self.dict_links = []
		self.limit = 10

	def json_to_dict(self, jsonStr):
		json_data = json.loads(jsonStr)
		return json_data

	def crawl(self, ID, depth):
		json_links = self.get_all_IDs(ID)

		# Do this depth first maybe? with better formatting and print to file
		for ID in json_links:
			IDs_in_ID = self.get_all_IDs(ID)
			for subID in IDs_in_ID:
				try:
					print(self.extract_words(subID).encode('utf-8'))
				except:
					print("no extracted area")

	def print_wiki_tree(self, ID, limit, depth):
		self.limit = limit
		self.depth_first_crawl(ID, depth)

	def depth_first_crawl(self, ID, depth):
		# Essentially a pre-order traversal

		if self.limit <= 0:
			print "end"
		elif depth == 0 and ID > 0:
			print str(self.limit) + ": " + ID
			self.limit -= 1
			print("----------------------------------------")
			print self.extract_words(ID).encode('utf-8')
			print "end node"
		else:
			possible_IDs = self.get_all_IDs(ID)
			for ID in possible_IDs:
				self.depth_first_crawl(ID, depth - 1)

	def get_source(self, link):
		webPage = urllib.urlopen(link)
		source = webPage.read()
		webPage.close()
		return source


	def get_page_id(self, wiki_link):
		source = self.get_source(wiki_link)
		index_of_ID = source.find("wgArticleId")
		index_of_ID = index_of_ID + 13

		ID = ""
		while is_number(source[index_of_ID]):
			ID = ID + source[index_of_ID]
			index_of_ID = index_of_ID + 1

		return ID

	def get_all_IDs(self, ID):
		link = self.get_API_link(ID)
		source = self.get_source(link)
		IDs = self.json_to_dict(source)
		if 'query' in IDs:
			IDs = [i for i in IDs['query']['pages'].keys() if IDs['query']['pages'][i]['ns'] == 0]
			return IDs
		else:
			return None

	def generate_link(self, ID):
		return "http://en.wikipedia.org/wiki/index.html?curid=" + ID

	def get_API_link(self, ID):
		#Reread the API for this, maybe search multiple IDs? pageids=ID|ID|ID
		return "http://en.wikipedia.org/w/api.php?action=query&format=json&pageids=" + ID + "&generator=links&gpllimit=max"

	def search_link(self, search):
		return "http://en.wikipedia.org/wiki/" + search.replace(" ", "_")


	def extract_words(self, ID):
		link = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&pageids=" + ID
		try:
			jsonified = self.json_to_dict(self.get_source(link))['query']['pages'][ID]
			if jsonified['ns'] == 0:
				return jsonified['extract']
			else:
				return None

		except:
			return "No extracts in this article"

	#currently not working, will make matrix soon
	def solve(self, init_search, end_search, max_depth):# initial = self.linkInit, final = self.linkFinal):
		ID_init = self.get_page_id(self.search_link(init_search))
		ID_end = self.get_page_id(self.search_link(end_search))

		graph = {
					ID_init : self.get_all_IDs(ID_init)
				}

		for ID in graph.keys():
			for subID in graph[ID]:
				if not subID in graph:
					graph[subID] = self.get_all_IDs(subID)

		print graph

	def backtrace(self, parent, start, end):
	    path = [end]

	    while path[-1] != start:
	        path.append(parent[path[-1]])
	    path.reverse()
	    return path




#print w.get_source("http://en.wikipedia.org/w/api.php?action=query&format=json&pageids=14627&generator=links&gpllimit=max")
#http://en.wikipedia.org/w/api.php?format=json&action=query&pageids=3258248|11524059&prop=extracts&excontinue=1&exlimit=4
#https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&exlimit=4&excontinue=&exsentences=5&pageids=3258248|14627|18978754
#print w.get_page_id(w.search_link("Isaac Newton"))
link = w.search_link("Isaac Newton")
ID = w.get_page_id(link)
w.print_wiki_tree(ID, 40, 5)
#links_on_page = w.get_all_IDs(ID)
#print ID
#words = w.extract_words(ID)
#print words.encode('utf-8')
#w.crawl(ID, 2)
#print w.extract_words(w.get_page_id(w.generate_link(links_on_page[3])))
#print w.solve("Isaac Newton", "Atom", 2)
