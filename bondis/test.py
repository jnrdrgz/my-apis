import requests
import json
from geopy.distance import geodesic

pos_cas = (-26.821118, -65.232977)
pos_av = (-26.824520, -65.234399)

#print(geodesic(pos_cas,pos_av).meters)

#with open('recorridos/4/colombres.json', 'r') as f:
#	points = json.load(f)

#points_and_distances = [(x,geodesic(x,pos_cas).meters) for x in points["puntos"]]
#print(sorted(points_and_distances, key=lambda x: x[1])[0])
#print(min([geodesic(pos_cas, x) for x in points]))

def get_distance_bondi_from_point(linea, ramal, coord):
	with open('recorridos/{}/{}.json'.format(linea, ramal), 'r') as f:
		points = json.load(f)

	points_and_distances = [(x,geodesic(x,pos_cas).meters) for x in points["puntos"]]
	#return sorted(points_and_distances, key=lambda x: x[1])[0]
	return min(points_and_distances,key=lambda x: x[1])

