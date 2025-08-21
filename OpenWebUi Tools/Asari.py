"""
title: Asari READ API Integration
author: Abstergo2003
author_url: https://github.com/Abstergo2003
funding_url: https://github.com/Abstergo2003
version: 2.0.0
"""

import os
import requests
import urllib.parse
import datetime
from pydantic import BaseModel, Field
import json
from timeit import default_timer as timer

schema_sources = {
    "ApartmentSale": "zFsreqfo",
    "ApartmentRental": "XXr34Wh3",
    "BuildingOffice": "e_WouSPL",
    "BuildingResidental": "BG2W00bg",
    "BuildingWarehouse": "MeNoatrm",
    "CommercialObjectRental": "n_628s2N",
    "CommercialObjectSale": "Pmb2fpO3",
    "CommercialSpaceRental": "LuG82IUH",
    "CommercialSpaceSale": "UG9sJvej",
    "HouseRental": "aR25grg1",
    "HouseSale": "u73S5wZq",
    "Investment": "3TtxjINx",
    "LotRental": "ILmPE__I",
    "LotSale": "D0fCcwZz",
    "RoomRental": "Ui68YYSN",
    "RoomSale": "KcDhFHqW",
    "WarehouseRental": "sa3icNJr",
    "WarehouseSale": "IlpgcGYW",
}


def fetch_listing_data(base_url, params):
    try:
        response = requests.post(base_url, headers=params)

        if response.status_code == 200:
            return response.json()["data"]
        else:
            print("Błąd:", response.status_code)
            print("Informacje:", response.text)
    except requests.RequestException as e:
        return f"Error fetching listing data: {str(e)}"


def query_listings(listingID, params):
    try:
        response = requests.post(
            f"https://api.asari.pro/site/listingList?query={listingID}", headers=params
        )

        if response.status_code == 200:
            return response.json()["data"][0]["id"]
        else:
            print("Błąd:", response.status_code)
            print("Informacje:", response.text)
    except requests.RequestException as e:
        return f"Error fetching listing data: {str(e)}"


def poi_prompt_builder(data):
    prompt = []
    for point in data:
        # prompt += f"""W pobliżu znajduje się {point["properties"].get("name")}. Na ulicy {point["properties"].get("street")} {point["properties"].get("housenumber")}.
        # Strona internetowa {point["properties"].get("website")}. Reszta kontaktu może być opisana: {point["properties"].get("contact")}. /n"""
        prompt.append(
            {
                "name": point["properties"].get("name"),
                "street": f"{point['properties'].get('street')} {point['properties'].get('housenumber')}",
                "website": point["properties"].get("website"),
                "contact": point["properties"].get("contact"),
            }
        )

    return prompt


def description_prompt_builder(data):
    url = ""
    prompt = ""
    sectionName = ""
    if data.get("section"):
        url = schema_sources[data["section"]]
        sectionName = data["section"].replace("Rental", "").replace("Sale", "")
    elif data.get("sectionName"):
        url = schema_sources[data["sectionName"]]
        sectionName = data["sectionName"]
    if url == "":
        return "No section found"

    with open(f"./open_webui/static/schemas/{url}.json", "r") as f:
        schema = json.load(f)

    for item in schema["boolean"]:
        if data.get(item["name"]):
            prompt += f"Obiekt {item['trans']} "

    for item in schema["dictionaryList"]:
        if data.get(item["name"]) != None:
            prompt += f"{item['trans']} {data[item['name']]}. "

    for item in schema["dictionary"]:
        if data.get(item["name"]) != None:
            prompt += f"{item['trans']} {data[item['name']]}. "

    for item in schema["float"]:
        if data.get(item["name"]) != None:
            prompt += f"{item['trans'].replace('{x}', str(data[item['name']]))}. "

    for item in schema["money"]:
        if data.get(item["name"]) != None:
            prompt += f"{item['trans']} {data[item['name']]}. "

    prompt += f"obiekt jest zlokalizowany w {data['location']}"

    return prompt.replace("Obiekt", sectionName)


class Tools:

    class Valves(BaseModel):
        API_TOKEN: str = Field("", description="Insert API key")
        USER_ID: str = Field("", description="Insert user id")
        MAP_API_TOKEN: str = Field("", description="Insert Geomapify api key")

    def __init__(self):
        self.valves = self.Valves()
        self.citation = True
        pass

    def get_description_of_listing(self, listingID: str) -> str:
        """
        Create description based on listing parameters in asari.
        :param listingID: string ID of listing on asari.
        :return: Listing information containing description.
        """
        if not listingID:
            return """ID has not been specified by user, solisting details can not be retrieved"""

        headers = {"SiteAuth": f"{self.valves.USER_ID}:{self.valves.API_TOKEN}"}
        id = query_listings(listingID, headers)

        base_url = f"https://api.asari.pro/site/listing?id={id}"

        data = fetch_listing_data(base_url, headers)

        prompt = description_prompt_builder(data)

        api_key = self.valves.MAP_API_TOKEN
        base_url = "https://api.geoapify.com/v2/places?"
        rad = "5000"
        response_loc = requests.get(
            f"""{base_url}apiKey={api_key}&filter=circle:{data["geoLng"]},{data["geoLat"]},{rad}&categories=activity,education,childcare,entertainment"""
        )
        data_loc = []
        if response_loc.status_code == 200:
            data_loc = response_loc.json()["features"]
        prompt_loc = poi_prompt_builder(data_loc)

        return f"""
            Twoim zadaniem jest stworzenie opisu nieruchomości z tych danych {prompt}. 
            Pamiętaj trzymać się wytycznych z bazy wiedzy oraz wzorować się na plikach wzorcowych. 
            Pamiętaj użyć list zamiast bloków tekstu.
            
            Jeżeli podane koniecznie zastosuj się do tych uwag:
            
            Szczegółowe wytyczne do poprawy:
                Opis ogłoszenia (największy priorytet):
                - Podział na sekcje tematyczne
                - Każda sekcja max 4-5 linijek
                - Dwa odstępy między sekcjami
                - Wyróżnienie najważniejszych informacji (**pogrubienie**)
                - Sekcje: lokalizacja, ekspozycja, dodatkowe udogodnienia
                - Unikanie "litanii" - ciągłego tekstu
                - Brak linków do zewnętrznych stron
                - Wyszczególnij dostępne środki transportu miejskiego
            
            Kompletność parametrów:
                - Wypełnienie wszystkich pól pod galerią
                - Szczególna uwaga na działki i garaże
            
            Lokalizacja:
                - Precyzyjne oznaczenie pinezką
                - Problem z obszarami zamiast konkretnych punktów
            
            Ważne miejsca w pobliżu (already provided, do not request more):
            Poniżej znajduje się pełna lista ważnych miejsc w pobliżu.
            Nie pytaj o adres ani dokładniejszą lokalizację — masz już wszystkie potrzebne dane.
            Wypisz ważne miejsca w okolicy w formie tabelki, podaj wszystkie dostępne informacje: tkaie jak nazwa, adress i kontakt
            {json.dumps(prompt_loc, indent=4)}
        """
