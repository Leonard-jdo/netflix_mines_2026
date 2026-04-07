from fastapi import FastAPI
from pydantic import BaseModel
from db import get_connection

app = FastAPI()


@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/films")
def get_films(page:int = 1, per_page:int = 10):
    with get_connection() as conn:
        cursor = conn.cursor()
        offset = (page-1)*per_page
        limit = per_page
        cursor.execute(f"""
SELECT * FROM Film LIMIT {limit} OFFSET {offset}
""")
        res = cursor.fetchall()
        print(res)
        return res 


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
