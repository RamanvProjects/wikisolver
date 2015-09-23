import urllib
import json
import time
from Queue import PriorityQueue

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def backtrace(parent, start, end):
    path = [end]

    while path[-1] != start:
        path.append(parent[path[-1]])

    path.reverse()
    return path

def aStarSearch(graph, h, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))

    cost = {}
    cost[start] = 0

    parents = {}
    while not frontier.empty():
        _, current = frontier.get()

        if current == goal:
            return backtrace(parents, start, goal)

        successors = graph[current]

        for successor in successors:
            cost[successor] = cost[current] + graph[current][successor]

            parents[successor] = current
            frontier.put((h[successor] + cost[successor], successor))

def djiskra(graph, start, goal):
    print start, goal
    frontier = PriorityQueue()
    frontier.put((0, start))

    cost = {}
    cost[start] = 0

    visited = set([start])
    parents = {}
    while not frontier.empty():
        #print graph
        c, current = frontier.get()
        print current, c
        if current == goal:
            return backtrace(parents, start, goal)

        try:
            if current not in graph:
                graph[current] = set([x for x in get_all_IDs(current) if x != current])
        except:
            graph[current] = set([])

        successors = graph[current]



        for successor in successors:
            new_cost = cost[current] + 1
            if successor not in visited:# or new_cost < cost[successor]:
                cost[successor] = new_cost
                visited.add(successor)
                parents[successor] = current
                if successor == goal:
                    return backtrace(parents, start, goal)
                frontier.put((cost[successor], successor))


def get_page_id(wiki_link):
	source = get_source(wiki_link)
	index_of_ID = source.find("wgArticleId")
	index_of_ID = index_of_ID + 13

	ID = ""
	while is_number(source[index_of_ID]):
		ID = ID + source[index_of_ID]
		index_of_ID = index_of_ID + 1

	return ID

def get_all_IDs(ID):
	link = get_API_link(ID)
	source = get_source(link)
	IDs = json_to_dict(source)
	if 'query' in IDs:
		IDs = [i for i in IDs['query']['pages'].keys() if IDs['query']['pages'][i]['ns'] == 0]
		return IDs
	else:
		return None

def get_API_link(ID):
	#Reread the API for this, maybe search multiple IDs? pageids=ID|ID|ID
	return "http://en.wikipedia.org/w/api.php?action=query&format=json&pageids=" + ID + "&generator=links&gpllimit=max"

def get_source(link):
	webPage = urllib.urlopen(link)
	source = webPage.read()
	webPage.close()
	return source

def json_to_dict(jsonStr):
    json_data = json.loads(jsonStr)
    return json_data

def generate_link(ID):
	return "http://en.wikipedia.org/wiki/index.html?curid=" + ID

def search_link(search):
	return "http://en.wikipedia.org/wiki/" + search.replace(" ", "_")

graph = {}
pageid = get_page_id("https://en.wikipedia.org/wiki/Isaac_Newton")
graph[pageid] = get_all_IDs(pageid)

print map(lambda x : generate_link(x), djiskra(graph, get_page_id("https://en.wikipedia.org/wiki/Isaac_Newton"), get_page_id("https://en.wikipedia.org/wiki/Hitler")))
