import requests 

URL = "http://www.tucuman.miredbus.com.ar/"

BONDIS = {
	"4":["5","6"],
	"5":["17","18","121"],
	"100":["101","102","103","104"],
	"102":["115","116","117"],
	"118":["134","135","136","137","138","299"],
	"130":["17","18"],
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

def get_all_bondis_of_line_pos(nro):
	pos = {NOMBRES[str(x)]: get_bondi_pos(x) for x in BONDIS[str(nro)]}
	return pos

def get_all_bondi_numbers():
	return {"numeros": list(BONDIS.keys())}
