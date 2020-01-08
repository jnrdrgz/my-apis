from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from dictio.get_words import get_word_defs
from bondis.get_data_bondis import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## test if working ##
@app.get("/working")
def read_root():
	return {"Working": True}

## dictionary ##
@app.get("/dictionary/{lang}/{word}")
def read_item(lang: str, word: str):
	w = {"Error": "Language not recognized"}
	if lang == "en":
		w = get_word_defs("en", word)
	if lang == "es":
		w = get_word_defs("es", word)
	
	return w

## bondis ##
@app.get("/bondis/{t}/{nro}")
def get_b(t: str, nro: str):
	jso = {"Error": "not type or line"}
	if t == "r":
		## hay dos metodos, uno trae la linea de la api de redbus
		## otro usa los recorridos guardados en memoria
		jso = get_all_bondis_of_line_rec_from_mem(nro)
	if t == "p":
		jso = get_all_bondis_of_line_pos(nro)
	
	return jso

@app.get("/bondis/lineas")
def get_lineas():
	return get_all_bondi_numbers()

@app.get("/bondis/cual_tomo/")
def get_lineas(plat: float = 0.0,plng: float = 0.0,dlat: float = 0.0,dlng: float = 0.0):
	return {"posibles": what_bondi_me_tomo((plat,plng),(dlat,dlng))}

#http://127.0.0.1:8000/bondis/cual_tomo/?plat=-26.822430&plng=-65.233187&dlat=-26.811059&dlng=-65.302625