from sqlalchemy.orm import Session
import models, schemas

def get_movies(db: Session):
    return db.query(models.Movie).all()

def get_movie(db: Session, movie_id:int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# Update with put
def update_movie(db: Session, movie_id: int, movie: schemas.MovieUpdate):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    db_movie.title = movie.title
    db_movie.overview = movie.overview
    db_movie.year = movie.year

    db.commit()
    db.refresh(db_movie)
    return db_movie

# Update with patch
def patch_movie(db: Session, movie_id: int, movie: schemas.MovieUpdate):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    update_data = movie.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_movie, key, value)

    db.commit()
    db.refresh(db_movie)

    return db_movie

def delete_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    db.delete(movie)
    db.commit()
    return movie
