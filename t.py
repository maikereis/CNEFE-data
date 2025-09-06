import json
import pandas as pd

d1 = pd.read_csv("data/extracted/adresses/11_RO.csv", sep=';', dtype={"COD_UF": "O",
                                                                      "COD_MUNICIPIO":"O",
                                                                      "COD_DISTRITO":"O",
                                                                      "COD_SUBDISTRITO":"O"
                                                                      })

with open("data/processed/metadata/state_mapping.json") as file:
    sta_mapping = json.load(file)

with open("data/processed/metadata/municipality_mapping.json") as file:
    mun_mapping = json.load(file)

with open("data/processed/metadata/distrital_mapping.json") as file:
    dis_mapping = json.load(file)

with open("data/processed/metadata/subdistrital_mapping.json") as file:
    sub_mapping = json.load(file)

print(sta_mapping)

d1["UF"]=d1["COD_UF"].map(sta_mapping)

d1["MUNICIPIO"]=d1["COD_MUNICIPIO"].map(mun_mapping)

d1["DISTRITO"]=d1["COD_DISTRITO"].map(mun_mapping)

d1["SUBDISTRITO"]=d1["COD_SUBDISTRITO"].map(mun_mapping)

print(d1)
