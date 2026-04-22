import os
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, database, data

app = FastAPI()


models.Base.metadata.create_all(bind=database.engine)


base_path = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_path, "templates"))


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def seed_db():
    db = database.SessionLocal()
    if db.query(models.Character).count() == 0:
        for char_data in data.CHARACTERS_DATA:
            new_char = models.Character(**char_data)
            db.add(new_char)
        db.commit()
    db.close()


@app.api_route("/", methods=["GET", "HEAD"])
def home(request: Request, db: Session = Depends(get_db)):
    chars = db.query(models.Character).all()
    return templates.TemplateResponse("index.html", {"request": request, "characters": chars})


@app.get("/api/characters")
def get_all_characters(db: Session = Depends(get_db)):
    return db.query(models.Character).all()


@app.get("/api/characters/{name}")
def get_character(name: str, db: Session = Depends(get_db)):
    return db.query(models.Character).filter(models.Character.name.ilike(name)).first()


@app.get("/api/actors")
def get_actors(db: Session = Depends(get_db)):
    chars = db.query(models.Character).all()
    return [
        {
            "character": c.name, 
            "voice_actor": c.voice_actor, 
            "singing_voice": c.singing_voice
        } for c in chars
    ]
