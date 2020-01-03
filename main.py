from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from dictio.get_words import get_word_defs
from bondis.get_data_bondis import *

app = FastAPI()
#uvicorn main:app --reload

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
		jso = get_all_bondis_of_line_rec(nro)
	if t == "p":
		jso = get_all_bondis_of_line_pos(nro)
	
	return jso

