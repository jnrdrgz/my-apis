import requests 
import json
from geopy.distance import geodesic


URL = "http://www.tucuman.miredbus.com.ar/"

BONDIS = {
	"4":["5","6"],
	"5":["17","18","121"],
	"100":["101","102","103","104"],
	"102":["115","116","117"],
	"118":["134","135","136","137","138","299"],
	"130":["185","186"],
}

NOMBRES = {

#4
"5":"Colombres", "6":"Mercofrut",
#5
"17":"Agrimensor","18":"Oeste","121":"105",
#100
"101":"Agric","102":"Santa Fe","103":"Gral Paz","104":"Avellaneda",
#102
"115":"Horco Molle", "116": "Rinconada", "117":"Los Pinos",
#118
"134":"APUNT","135":"200","136":"Rinconada","137":"Pie del Cerro","138":"Zona Sur","299":"San Javier",
#130
"185":"Ruta 9", "186":"San Jose",

}

def get_codes_all_lineas():
	url = URL + "/rest/lineas/0"
	r = requests.get(url).json()
	bondis = {} 
	for x in r["lineas"]:
		n = x["descripcion"].split("-")[0].replace("Linea","").strip()
		bondis[n] = []
	for x in r["lineas"]:
		n = x["descripcion"].split("-")[0].replace("Linea","").strip()
		bondis[n].append(x["codLinea"])

	return bondis

def get_bondi_pos(code):
	r = requests.get(URL + "rest/posicionesBuses/" + str(code)).json()

	#pos = [{"latitud": (x["latitud"], "longitud": x["longitud"]), "orientacion":x["orientacion"] for x in r["posiciones"]]
	#print(r)

	return r

def get_bondi_rec(bond_code):
	r = requests.get(URL + "rest/rutaLinea/" + str(bond_code)).json()
	
	points = {"puntos": [[x["latitud"], x["longitud"]] for x in r["nodos"]]}
	return points

def get_all_bondis_of_line_rec(nro):
	recs = {NOMBRES[str(x)]: get_bondi_rec(x) for x in BONDIS[str(nro)]}
	return recs

## para los metodos de busqueda de recorrido y similares, es mejor tener los recorridos descargados
## y traerlos directamente de los archivos json, ya que si no habría que llamar a la api de redbus
## cada vez que se pidan los recorridos
def get_all_bondis_of_line_rec_from_mem(nro):
	recs = []
	for k in BONDIS[str(nro)]:
		with open('bondis/recorridos/{}/{}.json'.format(nro,NOMBRES[k]), 'r') as f:
			recs.append(json.load(f))
	
	return recs

def get_all_bondis_of_line_pos(nro):
	pos = {NOMBRES[str(x)]: get_bondi_pos(x) for x in BONDIS[str(nro)]}
	return pos

def get_all_bondi_numbers():
	return {"numeros": list(BONDIS.keys())}

def download_rec(linea,ramal):
	with open('bondis/recorridos/{}/{}.json'.format(linea,ramal), 'w') as f:
		json.dump(get_all_bondis_of_line_rec(linea)[ramal],f)

def download_all_recs_json():
	for k in BONDIS.keys():
		for c in BONDIS[k]:
			download_rec(k,NOMBRES[c])

def get_distance_bondi_from_point(linea, ramal, coord):
	with open('bondis/recorridos/{}/{}.json'.format(linea, ramal), 'r') as f:
		points = json.load(f)

	points_and_distances = [(x,geodesic(x,coord).meters) for x in points["puntos"]]
	#return sorted(points_and_distances, key=lambda x: x[1])[0]
	return min(points_and_distances,key=lambda x: x[1])

def what_bondi_me_tomo(partida, destino):
	posibles = []
	for k in BONDIS.keys():
		for c in BONDIS[k]:
			d_partida = get_distance_bondi_from_point(k,NOMBRES[c],partida)
			d_destino = get_distance_bondi_from_point(k,NOMBRES[c],destino)
			
			if(d_partida[1] <= 500 and d_destino[1] <= 500):
				posibles.append([k,NOMBRES[c]])

	return posibles

def what_bondi_pasan_por_aca(punto):
	posibles = []
	for k in BONDIS.keys():
		for c in BONDIS[k]:
			d_destino = get_distance_bondi_from_point(k,NOMBRES[c],punto)
			
			if(d_partida[1] <= 500):
				posibles.append([k,NOMBRES[c]])

	return posibles
