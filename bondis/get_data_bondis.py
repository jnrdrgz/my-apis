import requests 

URL = "http://www.tucuman.miredbus.com.ar/"

BONDIS = {
	"102":["115","116","117"],
}

NOMBRES = {

#102
"115":"Horco Molle", "116": "Rinconada", "117":"Los Pinos",

}

def get_bondi_pos(code):
	r = requests.get(URL + "rest/posicionesBuses/" + str(code)).json()

	#pos = [{"latitud": (x["latitud"], "longitud": x["longitud"]), "orientacion":x["orientacion"] for x in r["posiciones"]]
	#print(r)

	return r

def get_bondi_rec(bond_code):
	r = requests.get(URL + "rest/rutaLinea/" + str(bond_code)).json()
	
	points = {"puntos": [[x["latitud"], x["longitud"]] for x in r["nodos"]]}
	return points

def get_all_bondis_of_line_pos(nro):
	pos = {NOMBRES[str(x)]: get_bondi_pos(x) for x in BONDIS[str(nro)]}
	return pos