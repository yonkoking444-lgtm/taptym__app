import os
from datetime import date
from pathlib import Path
from uuid import uuid4
from typing import List
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import Base, engine, ensure_car_columns, get_db
from .models import Car, UserProfile
from .schemas import CarCreate, CarResponse, CarTagsUpdate, CarUpdate, ProfileResponse, ProfileUpdate
Base.metadata.create_all(bind=engine)
ensure_car_columns()
app = FastAPI(title='Taptym Cars API', version='1.0.0')
UPLOAD_DIR = Path(__file__).resolve().parent.parent / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount('/uploads', StaticFiles(directory=UPLOAD_DIR), name='uploads')
app.add_middleware(CORSMiddleware, allow_origins=[os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

def current_date_label() -> str:
    months = (
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря',
    )
    today = date.today()
    return f'{today.day} {months[today.month - 1]} {today.year} г.'

@app.get('/')
def root() -> dict:
    return {
        'name': 'Taptym Cars API',
        'status': 'ok',
        'health': '/api/health',
        'cars': '/api/cars',
        'seller_cars': '/api/seller-cars',
        'buyer_requests': '/api/buyer-requests',
        'docs': '/docs',
    }
@app.get('/api/health')
def health() -> dict:
    return {'status': 'ok'}
@app.get('/api/profiles', response_model=List[ProfileResponse])
def list_profiles(db: Session = Depends(get_db)) -> List[UserProfile]:
    return list(db.query(UserProfile).order_by(UserProfile.id).all())
@app.get('/api/profiles/{email}', response_model=ProfileResponse)
def get_profile(email: str, db: Session = Depends(get_db)) -> UserProfile:
    profile = db.query(UserProfile).filter(UserProfile.email == email).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Profile not found')
    return profile
@app.put('/api/profiles/{email}', response_model=ProfileResponse)
def update_profile(email: str, payload: ProfileUpdate, db: Session = Depends(get_db)) -> UserProfile:
    profile = db.query(UserProfile).filter(UserProfile.email == email).first()
    if profile is None:
        profile = UserProfile(email=email)
        db.add(profile)
    values = payload.model_dump(exclude_unset=True, by_alias=True)
    if 'imageUrl' in values:
        values['image_url'] = values.pop('imageUrl')
    for field, value in values.items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile
@app.post('/api/uploads')
async def upload_image(file: UploadFile = File(...)) -> dict:
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only image files are allowed')
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail='Image must be smaller than 10 MB')
    extension = Path(file.filename or '').suffix.lower()
    if extension not in {'.jpg', '.jpeg', '.png', '.webp', '.gif'}:
        extension = '.bin'
    filename = f'{uuid4().hex}{extension}'
    (UPLOAD_DIR / filename).write_bytes(content)
    public_url = os.getenv('API_PUBLIC_URL', 'http://localhost:8000')
    return {'url': f'{public_url}/uploads/{filename}'}
@app.get('/api/cars', response_model=List[CarResponse])
def list_cars(db: Session = Depends(get_db)) -> List[Car]:
    return list(db.scalars(select(Car).order_by(Car.id)))
@app.get('/api/seller-cars', response_model=List[CarResponse])
def list_seller_cars(db: Session = Depends(get_db)) -> List[Car]:
    return list(db.scalars(select(Car).where(Car.action == 'Продам').order_by(Car.id)))
@app.get('/api/buyer-requests', response_model=List[CarResponse])
def list_buyer_requests(db: Session = Depends(get_db)) -> List[Car]:
    return list(db.scalars(select(Car).where(Car.action == 'Куплю').order_by(Car.id)))
def create_car_record(payload: CarCreate, db: Session) -> Car:
    values = payload.model_dump()
    values['date'] = values.get('date') or current_date_label()
    car = Car(**values)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car
@app.post('/api/cars', response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(payload: CarCreate, db: Session = Depends(get_db)) -> Car:
    return create_car_record(payload, db)
@app.post('/api/seller-cars', response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_seller_car(payload: CarCreate, db: Session = Depends(get_db)) -> Car:
    payload.action = 'Продам'
    return create_car_record(payload, db)
@app.post('/api/buyer-requests', response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_buyer_request(payload: CarCreate, db: Session = Depends(get_db)) -> Car:
    payload.action = 'Куплю'
    return create_car_record(payload, db)
@app.get('/api/profiles/{email}/cars', response_model=List[CarResponse])
def list_profile_cars(email: str, db: Session = Depends(get_db)) -> List[Car]:
    return list(db.scalars(select(Car).where(Car.owner_email == email).order_by(Car.id)))
@app.get('/api/cars/{car_id}', response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)) -> Car:
    car = db.get(Car, car_id)
    if car is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')
    return car
@app.put('/api/cars/{car_id}', response_model=CarResponse)
def update_car(car_id: int, payload: CarUpdate, db: Session = Depends(get_db)) -> Car:
    car = db.get(Car, car_id)
    if car is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(car, field, value)
    db.commit()
    db.refresh(car)
    return car
@app.delete('/api/cars/{car_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, db: Session = Depends(get_db)) -> None:
    car = db.get(Car, car_id)
    if car is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')
    db.delete(car)
    db.commit()
@app.put('/api/cars/{car_id}/tags', response_model=CarResponse)
def update_car_tags(car_id: int, payload: CarTagsUpdate, db: Session = Depends(get_db)) -> Car:
    car = db.get(Car, car_id)
    if car is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')
    car.tags = payload.tags
    db.commit()
    db.refresh(car)
    return car
