import unittest
import re

def distanceToCollectKeys(currentKey, Graph_A, cache=None,keys_collected=None):
	if keys_collected==None:
		keys_collected=[]
	else:
		keys_collected=keys_collected+currentKey
		keys_collected = list(dict.fromkeys(keys_collected))
		keys_collected=list(set(keys_collected) - set(['<','>','^','+']))
	keys_all=list(set([x[1] for x in Graph_A.path_dict_tmp.keys() if ('+' in x[0]) ]) - set(['<','>','^']))
	if keys_collected!=[]:
		keys_remaining=list(set(keys_all) - set(keys_collected))
	else:
		keys_remaining=keys_all
	if keys_remaining==[]:
		return [0,cache]
	cacheKey = str((currentKey, set(keys_remaining)))
	if cache!=None:
		if cacheKey in cache.keys():
			return [cache[cacheKey],cache]
	result = 10000000000000
	reachable_keys_1=[]
	for robot_1 in currentKey:
		reachable_keys_1=reachable_keys_1+get_all_reachable_keys(Graph_A,robot_1,keys_collected)
	for key in reachable_keys_1:
		for robot in currentKey:
			if Graph_A.path_dict_tmp[key+ robot]!='Route Not Possible':
				guaranteed_new_distance=len(Graph_A.path_dict_tmp[key+ robot])
				break
		currentKey_tmp=[key if value==robot else value for value in currentKey]
		[new_distance,cache]=distanceToCollectKeys(list(currentKey_tmp), Graph_A, cache,keys_collected)
		d = guaranteed_new_distance - 1 + new_distance
		result = min([result, d])
	if cache==None:
		cache={}
	cache[cacheKey] = result
	if currentKey==['<','^','>','+']:
		return result
	return [result,cache]


def read_distances(filename):
	dists = []
	with open(filename, 'rb') as f:
		for line in f:
			# Skip comments
			if line[0] == '#':
				continue
			print('map(str.strip, line.split(','))',map(str.strip, line.split(',')))
			dists.append(map(int, map(str.strip, line.split(','))))
	return dists

def get_all_reachable_keys(Graph_A,current_location,collected_keys=None):
	if collected_keys==None:collected_keys=[]
	path_dict=Graph_A.path_dict_tmp
	all_keys=get_all_keys(Graph_A)
	all_doors=get_all_doors(Graph_A)
	reachable_keys=[]
	for key1 in collected_keys:
		all_keys.remove(key1)
	for key1 in collected_keys:
		if key1.upper() in  all_doors:
			all_doors.remove(key1.upper())
	set_all_doors=set(all_doors)
	set_all_keys=set(all_keys)
	len_all_keys=len(all_keys)
	len_all_doors=len(all_doors)
	for key1 in all_keys:
		stop=0
		path_tmp=path_dict[key1+current_location]
		set_path_tmp=set(path_tmp[1:-1])
		if len_all_doors>0:
			if len((set_all_doors & set_path_tmp))>0:
				stop=1
		if len_all_keys>0 and stop==0:
			if len((set_all_keys & set_path_tmp))>0:
				stop=1
		if stop==0:
			reachable_keys=reachable_keys+[key1]
	return reachable_keys

def get_all_keys(A):
	return re.findall('([a-z])', str(list(A.edges())))

def get_all_doors(A):
	return re.findall('([A-Z])', str(list(A.edges())))

def dijsktra(graph, initial, end):
	shortest_paths = {initial: (None, 0)}
	current_node = initial
	visited = set()
	while current_node != end:
		visited.add(current_node)
		destinations = graph.edges()[current_node]
		weight_to_current_node = shortest_paths[current_node][1]
		for next_node in destinations:
			weight = graph.weights(current_node, next_node) + weight_to_current_node
			if next_node not in shortest_paths:
				shortest_paths[next_node] = (current_node, weight)
			else:
				current_shortest_weight = shortest_paths[next_node][1]
				if current_shortest_weight > weight:
					shortest_paths[next_node] = (current_node, weight)
		next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
		if not next_destinations:
			return "Route Not Possible"
		current_node = min(next_destinations, key=lambda k: next_destinations[k][1])	
	path = []
	while current_node is not None:
		path.append(current_node)
		next_node = shortest_paths[current_node][0]
		current_node = next_node
	path = path[::-1]
	return path

def enumerate_empty_positions(test_maze_1):
	a=0
	robot=['<','^','>','+']
	for i in range(len(test_maze_1)):
		for j in range(len(test_maze_1[0])):
			if test_maze_1[i][j]=='.':
				test_maze_1[i][j]=str(a)
				a=a+1
			if test_maze_1[i][j]=='@':
				test_maze_1[i][j]=robot[0]
				robot.remove(robot[0])
	return test_maze_1

def get_maze_location(test_maze_1,symbol):
	for i, e in enumerate(test_maze_1):
		try:
			return [e.index(symbol),i]
		except ValueError:
			pass
	return -1

def get_maze(filename_1):
	return get_maze_read(open(filename_1))


def get_maze_read(f):
	return convert_to_2D_list(f.readlines())

def convert_to_2D_list(array):
	if len(array)>1:
		return [list(array[0].rstrip())]+convert_to_2D_list(array[1:])
	else:
		return [list(array[0].rstrip())]

def get_graph_dict_all(test_maze_complete):
	dict_all={}
	for j in range(len(test_maze_complete)):
		for i in range(len(test_maze_complete[0])):
			if test_maze_complete[j][i]!='#':
				dict_all.update(get_graph_dict_symbol(test_maze_complete,test_maze_complete[j][i]))
	return dict_all

def get_graph_dict_symbol(test_maze_complete,symbol):
	location_1=get_maze_location(test_maze_complete,symbol)
	dict_1={}
	list_tmp=[]
	for i in range(location_1[0]-1,location_1[0]+2):
		try:
			if test_maze_complete[location_1[1]][i]!='#' and test_maze_complete[location_1[1]][i]!=symbol:
				list_tmp=list_tmp+[test_maze_complete[location_1[1]][i]]
		except:
			pass
	for j in range(location_1[1]-1,location_1[1]+2):
		try:
			if test_maze_complete[j][location_1[0]]!='#' and test_maze_complete[j][location_1[0]]!=symbol:
				list_tmp=list_tmp+[test_maze_complete[j][location_1[0]]]
		except:
			pass
	dict_1[symbol]=list_tmp
	return dict_1

class Graph(object):
	def __init__(self, graph_dict=None):
		if graph_dict == None:
			graph_dict = {}
		self.__graph_dict = graph_dict
		self.max_number=-10
		self.path_dict_tmp={}
	def edges(self):
		return self.__generate_edges()
	def weights(self,current_node,next_node):
		if next_node in self.__graph_dict[current_node]:
			return 1
		else:
			return 100000000000000000000
	def __generate_edges(self):
		return self.__graph_dict

def get_all_keys_distances(A):
	all_keys=get_all_keys(A)+['<','^','>','+']
	path_dict={}
	for i in range(len(all_keys)):
		for j in range(len(all_keys)):
			if all_keys[i]!=all_keys[j]:
				path_dict[all_keys[i]+all_keys[j]]=dijsktra(A,all_keys[i],all_keys[j])
	return path_dict

class LearningCase(unittest.TestCase):
	def test_starting_out(self):
#		self.assertEqual(get_maze("test_2.txt"),[['#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', 'b', '.', 'A', '.', '@', '.', 'a', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#']])
#		self.assertEqual(enumerate_empty_positions(get_maze("test_3.txt")),[['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', 'f', '0', 'D', '1', 'E', '2', 'e', '3', 'C', '4', 'b', '5', 'A', '6', '@', '7', 'a', '8', 'B', '9', 'c', '10', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '11', '#'], ['#', 'd', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']])
#		self.assertEqual((get_graph_dict_all(enumerate_empty_positions(get_maze("test_5.txt")))),{'i': ['0'], '0': ['i', 'G'], 'G': ['0', '1'], '1': ['G', '2'], '2': ['1', 'c'], 'c': ['2', '3'], '3': ['c', '4'], '4': ['3', '5', '9'], '5': ['4', 'e'], 'e': ['5', '6'], '6': ['e', '7'], '7': ['6', 'H'], 'H': ['7', '8'], '8': ['H', 'p'], 'p': ['8'], '9': ['4', '14'], 'j': ['10'], '10': ['j', 'A'], 'A': ['10', '11'], '11': ['A', '12'], '12': ['11', 'b'], 'b': ['12', '13'], '13': ['b', '14'], '14': ['13', '15', '9', '@'], '15': ['14', 'f'], 'f': ['15', '16'], '16': ['f', '17'], '17': ['16', 'D'], 'D': ['17', '18'], '18': ['D', 'o'], 'o': ['18'], '@': ['14', '23'], 'k': ['19'], '19': ['k', 'E'], 'E': ['19', '20'], '20': ['E', '21'], '21': ['20', 'a'], 'a': ['21', '22'], '22': ['a', '23'], '23': ['22', '24', '@', '28'], '24': ['23', 'g'], 'g': ['24', '25'], '25': ['g', '26'], '26': ['25', 'B'], 'B': ['26', '27'], '27': ['B', 'n'], 'n': ['27'], '28': ['23', '33'], 'l': ['29'], '29': ['l', 'F'], 'F': ['29', '30'], '30': ['F', '31'], '31': ['30', 'd'], 'd': ['31', '32'], '32': ['d', '33'], '33': ['32', '34', '28'], '34': ['33', 'h'], 'h': ['34', '35'], '35': ['h', '36'], '36': ['35', 'C'], 'C': ['36', '37'], '37': ['C', 'm'], 'm': ['37']})
#		print(enumerate_empty_positions(get_maze("puzzle_input_2.txt")))
		A1_tmp=Graph(get_graph_dict_all(enumerate_empty_positions(get_maze("test_second_1.txt"))))
		A1_tmp.path_dict_tmp=get_all_keys_distances(A1_tmp)
		A2_tmp=Graph(get_graph_dict_all(enumerate_empty_positions(get_maze("test_second_2.txt"))))
		A2_tmp.path_dict_tmp=get_all_keys_distances(A2_tmp)
		A3_tmp=Graph(get_graph_dict_all(enumerate_empty_positions(get_maze("test_second_3.txt"))))
		A3_tmp.path_dict_tmp=get_all_keys_distances(A3_tmp)
		puzzle_tmp=Graph(get_graph_dict_all(enumerate_empty_positions(get_maze("puzzle_input_2.txt"))))
		puzzle_tmp.path_dict_tmp=get_all_keys_distances(puzzle_tmp)
		
		robot=['<','^','>','+']
		
		self.assertEqual(distanceToCollectKeys(['<','^','>','+'], A1_tmp),8)
		self.assertEqual(distanceToCollectKeys(['<','^','>','+'], A2_tmp),24)
		self.assertEqual(distanceToCollectKeys(['<','^','>','+'], A3_tmp),32)
		self.assertEqual(distanceToCollectKeys(['<','^','>','+'], puzzle_tmp),2138)

def main():
	unittest.main()

if __name__ == "__main__":
	main()
