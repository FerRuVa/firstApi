from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime


app = FastAPI()

#Coments importans for code in FastAPI
#-------------- Validatons -------------
# gt greater than >
# ge greater than or equal >=
# lt less than <
# le less than or equal <=

class Movie(BaseModel):
    id: int
    title:str
    overview: str
    year:int
    rating:float
    category:str

class MovieCreate (BaseModel):
    id: int
    title:str = Field(min_length=5, max_length=15, default='My movie')
    overview: str = Field(min_length=15, max_length=50)
    year:int = Field(le=datetime.date.today().year, ge=1900)
    rating:float = Field(ge=0, le=10)
    category:str = Field(min_length=5, max_length=20)
    #Valores por defecto
    model_config = {
        'json_schema_extra':{
            'example': {
                'id': 1,
                'title': 'My movie',
                'overview': 'This Movie is about...',
                'rating': 10,
                'year': 2025,
                'category': 'Comedy'
            }
        }
    }

#class MovieUpdate(BaseModel):
   # title: str | None = Field(default=None, min_length=15, max_length=30)
   # overview: str | None = Field(default=None, min_length=15, max_length=50)
   # year: int | None = Field(default=None, ge=1900, le=datetime.date.today().year)
   # rating: float | None = Field(default=None, ge=0, le=10)
   # category: str | None = Field(default=None, min_length=5, max_length=20)

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    category: Optional[str] = None


movies = [
    {
    "id": 1,
    "title": "Avatar",
    "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
    "year": "2009",
    "rating": 7.8,
    "category": "Acción"
    },
    {
    "id": 4,
    "title": "Avatar2",
    "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
    "year": "2009",
    "rating": 7.8,
    "category": "Comedia"
    },
    {
    "id": 2,
    "title": "Avatar3",
    "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
    "year": "2009",
    "rating": 7.8,
    "category": "Acción"
    }
]

app.title = "Mi primer API"
app.version = "2.0.0"

@app.get('/', tags=["Home"])


def home():
    return "Hola mundo! ::://"


@app.get('/movies', tags=["Movies"])
def get_movies() -> List[Movie]:
    return movies

@app.get('/movies/{id}', tags=["Movies"])
def get_movie(id: int) -> Movie:
    for movie in movies:
        if  movie['id'] == id:
            return movie
    return []

@app.get('/movies/', tags=["Movies"])
def get_movie_by_category(category: str) -> Movie:
    for movie in movies:
        if  movie['category'] == category:
            return movie
    return []

@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(
        movie.model_dump()
    )
    return movies

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(
        id: int, movie: MovieUpdate
        )-> List[Movie]:
        for item in movies:
            if  item['id'] == id:
                item['title'] = movie.title
                item['overview'] = movie.overview
                item['year'] = movie.year
                item['rating'] = movie.rating
                item['category'] = movie.category
        return movies

@app.patch('/movies/{id}')
def update_movie_patch(id: int, movie: MovieUpdate):

    for item in movies:
        if item['id'] == id:

            update_data = movie.model_dump(exclude_unset=True)

            for key, value in update_data.items():
               item[key] = value

            return item

    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int) -> List[Movie]:
    for movie in movies:
            if  movie['id'] == id:
                movies.remove(movie)
    return movies
