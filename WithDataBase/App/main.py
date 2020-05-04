from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
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
    Company: str
    Address: str
    City: str
    State: str
    Country: str
    Postalcode: str
    Fax: str

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
        "SELECT * FROM tracks ORDER BY TrackId ASC LIMIT ? OFFSET ?;"
        , (per_page, page )).fetchall()
    return data

@app.get("/albums/{album_id}")
async def get_album_by_id(album_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(    "SELECT * FROM albums WHERE AlbumId = ?;"     , (album_id, )).fetchone()
    return data


@app.get("/tracks/composer/")
async def track_composer(composer_name: str = Query(None)):
    app.db_connection.row_factory = lambda cursor, x: x[0]

    data = app.db_connection.execute(    'SELECT composer FROM tracks WHERE Composer = ?;' , (composer_name, )  ).fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail={"error": "str"})

    data = app.db_connection.execute(        'SELECT name FROM tracks WHERE composer = ?;' ,(composer_name, )  ).fetchall()
    return data

@app.post("/albums", response_model=AlbumResp, status_code=201)
async def post_album(req: AlbumRq):

    app.db_connection.row_factory = lambda cursor, x: x[0]
    data = app.db_connection.execute(    "SELECT * FROM artists WHERE ArtistId = ?;"     , (req.artist_id, )).fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail={"error": "str"})
    
    app.db_connection.row_factory = sqlite3.Row

    cursor = app.db_connection.execute(    "INSERT INTO albums (Title, ArtistId) VALUES (?,?);"    , (req.title,req.artist_id )  )
    
    app.db_connection.commit()
    new_album_id = cursor.lastrowid

    return AlbumResp(AlbumId=new_album_id,Title=req.title,ArtistId=req.artist_id)


@app.put("/customers/{customer_id}", response_model=CustomerResp)
async def put_customer(customer_id: int, req : CustomerResp):

    app.db_connection.row_factory = sqlite3.Row

    data = app.db_connection.execute(    "SELECT * FROM customers WHERE CustomerId = ?;"     , (customer_id, )).fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail={"error": "str"})
    
    stored_item_data = data
    stored_item_model = CustomerResp(**stored_item_data)
    updated_data = req.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=updated_data)
    
    cursor = app.db_connection.execute(    "UPDATE customers SET FirstName= ?, LastName= ?, Company= ?, Address= ?, City= ?, State= ?, Country= ?, PostalCode= ?, Phone= ?, Fax=?, Email= ? WHERE CustomerId = ?;"    , 
    (updated_item.FirstName ,updated_item.LastName, updated_item.Company, updated_item.Address, updated_item.City, updated_item.State, updated_item.Country, updated_item.PostalCode, updated_item.Phone, updated_item.Fax, updated_item.Email, customer_id)  )
    app.db_connection.commit()

    return updated_item

@app.get("/sales")
async def get_sales(category: str = Query(None)):

    # check if parameter is customers
    app.db_connection.row_factory = sqlite3.Row
    #lambda cursor, x: x[0]

    if category == "customers":
        data = app.db_connection.execute(    "SELECT customers.CustomerId, Email, Phone, Total AS Sum FROM customers INNER JOIN invoices ON customers.CustomerId = invoices.InvoiceId ORDER BY Sum DESC, customers.CustomerId ASC;"  ).fetchall()
        
        return data
    
    if category == "genres":
        data = app.db_connection.execute(    "SELECT genres.Name, COUNT(genres.Name * invoice_items.Quantity) AS Sum FROM tracks JOIN genres ON tracks.GenreId = genres.GenreId JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId GROUP BY genres.Name ORDER BY Sum DESC, genres.Name ASC;"  ).fetchall()         
        return data
    
    
    
    raise HTTPException(status_code=404, detail={"error": "str"})
    
