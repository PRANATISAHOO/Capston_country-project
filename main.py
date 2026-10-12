from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3

from database import CountryDatabaseManger

app = FastAPI(title="Country Data API")
db = CountryDatabaseManger()

class Country(BaseModel):
    country_name: str = Field(min_length=1)
    capital: str 
    population: int = Field(ge=0)
    area: float = Field(ge=0)

@app.get("/")
def home():
    return {"message": "Welcome to the Country Data API"}

@app.get("/countries")
def get_countries():
    return db.get_all()
@app.get("/countries/{country_name}")
def get_country(country_name: str):
    country = db.get_by_name(country_name)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@app.post("/countries", status_code=201)
def create_country(country: Country):
    try:
        db.create(country.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Country already exists")
    return {"message": "Country created successfully", "country": country}

@app.put("/countries/{country_name}")
def update_country(country_name: str, country: Country):
    if country.country_name != country_name:
        raise HTTPException(status_code=400, detail="path name and country_name must match")
    if not db.update(country_name, country.model_dump()):
        raise HTTPException(status_code=404, detail="Country not found")
    return {"message": "Country updated"}

@app.delete("/countries/{country_name}")
def delete_country(country_name: str):
    if not db.delete(country_name):
        raise HTTPException(status_code=404, detail="Country not found")
    return {"message": "Country deleted"}
    