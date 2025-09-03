from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware

SQLALCHEMY_DB_URL = 'sqlite:///./data.db'
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ContactMessage(Base):
    __tablename__ = "contact_us"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, index=True)
    message = Column(String, index=True)

class ContactBase(BaseModel):
    fullname: str
    email: str
    message: str

class ContactCreate(ContactBase):
    pass

class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)

app = FastAPI()

ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contact/", response_model=ContactOut)
async def create_contact_message(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        db_contact = ContactMessage(**contact.dict())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")