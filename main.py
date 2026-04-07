from fastapi import FastAPI
from pydantic import BaseModel
from db import get_connection
import json

app = FastAPI()


@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/films/{id}")
def get_one_film(id:int):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM Film WHERE Film.ID = {id}""")   
        res = cursor.fetchone()
        return json(res)



@app.get("/films")
def get_films(page:int = 1, per_page:int = 20, genre_id:int=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        offset = (page-1)*per_page
        query=f"""SELECT * FROM Film"""
        if genre_id:
            query+=f""" WHERE Film.Genre_ID = {genre_id}"""
        query+=f""" LIMIT {per_page} OFFSET {offset}"""
        cursor.execute(query)   
        res = cursor.fetchall()
        return {
  "data": json(res),
  "page": page,
  "per_page": per_page,
  "total": 100
}






class Film(BaseModel):
    id: int | None = None
    nom: str
    note: float | None = None
    datesortie: int
    image: str | None = None
    video: str | None = None
    genreId: int | None = None


@app.post("/film")
async def createFilm(film : Film):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO Film (Nom,Note,DateSortie,Image,Video)  
            VALUES('{film.nom}',{film.note},{film.datesortie},'{film.image}','{film.video}') RETURNING *
            """)
        res = cursor.fetchone()
        print(res)
        return res


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
