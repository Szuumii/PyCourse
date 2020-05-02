from fastapi import FastAPI, HTTPException, Query, Request
#from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
import sqlite3

app = FastAPI()

class AlbumRq(BaseModel):
    title: str
    artist_id: int

class AlbumResp(BaseModel):
    AlbumId: int
    Title: str
    ArtistId: int

class CustomerRq(BaseModel):
    company: str
    address: str
    city: str
    state: str
    country: str
    postalcode: str
    fax: str

class CustomerResp(BaseModel):
    CustomerId: int = None
    FirstName: str = None
    LastName: str = None
    Company: str = None
    Address: str = None
    City: str = None
    State: str = None
    Country: str = None
    PostalCode: str = None
    Phone: str = None
    Fax: str = None
    Email: str = None
    SupportRepId: int = None
 


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/tracks/")
async def some_tracks(per_page: int = 10,page :int = 0):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT * FROM tracks ORDER BY TrackId ASC LIMIT ? OFFSET ?"
        , (per_page, page )).fetchall()
    return data

@app.get("/albums/{album_id}")
async def get_album_by_id(album_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(    "SELECT * FROM albums WHERE AlbumId = ?"     , (album_id, )).fetchone()
    return data


@app.get("/tracks/composer/")
async def track_composer(composer_name: str = Query(None)):
    app.db_connection.row_factory = lambda cursor, x: x[0]

    data = app.db_connection.execute(    'SELECT composer FROM tracks WHERE Composer = ?' , (composer_name, )  ).fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail={"error": "str"})

    data = app.db_connection.execute(        'SELECT name FROM tracks WHERE composer = ?' ,(composer_name, )  ).fetchall()
    return data

@app.post("/albums", response_model=AlbumResp, status_code=201)
async def post_album(req: AlbumRq):

    app.db_connection.row_factory = lambda cursor, x: x[0]
    data = app.db_connection.execute(    "SELECT * FROM artists WHERE ArtistId = ?"     , (req.artist_id, )).fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail={"error": "str"})
    
    app.db_connection.row_factory = sqlite3.Row

    cursor = app.db_connection.execute(    "INSERT INTO albums (Title, ArtistId) VALUES (?,?)"    , (req.title,req.artist_id )  )
    
    app.db_connection.commit()
    new_album_id = cursor.lastrowid

    return AlbumResp(AlbumId=new_album_id,Title=req.title,ArtistId=req.artist_id)


@app.get("/customers/{customer_id}", response_model=CustomerResp)
async def put_customer(customer_id: int):

    app.db_connection.row_factory = sqlite3.Row

    data = app.db_connection.execute(    "SELECT * FROM customers WHERE CustomerId = ?"     , (customer_id, )).fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail={"error": "str"})
    
    response = CustomerResp( CustomerId= customer_id, FirstName= data["FirstName"], LastName= data["LastName"], Company= data["Company"], Address= data["Address"], City= data["City"], State= data["State"], Country= data["Country"], PostalCode= data["PostalCode"], Phone= data["Phone"], Fax= data["Fax"], Email= data["Email"], SupportRepId= data["SupportRepId"])

    

    return response


    
