import os  
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, database, data

app = FastAPI()
base_path = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_path, "templates"))

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

@app.on_event("startup")
def seed_db():
    db = database.SessionLocal()
    if db.query(models.Character).count() == 0:
        for char in data.CHARACTERS_DATA:
            db.add(models.Character(**char))
        db.commit()
    db.close()

# UI Route (Cute Design)
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    chars = db.query(models.Character).all()
    return templates.TemplateResponse("index.html", {"request": request, "characters": chars})

# Feature 1: Get All Characters (JSON)
@app.get("/api/characters")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Character).all()

# Feature 2: Get Specific Character
@app.get("/api/characters/{name}")
def get_one(name: str, db: Session = Depends(get_db)):
    return db.query(models.Character).filter(models.Character.name.ilike(name)).first()

# Feature 3: Get Actors
@app.get("/api/actors")
def get_actors(db: Session = Depends(get_db)):
    chars = db.query(models.Character).all()
    return [{"character": c.name, "actor": c.voice_actor, "singer": c.singing_voice} for c in chars]