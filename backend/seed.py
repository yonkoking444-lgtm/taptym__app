from app.db import Base, SessionLocal, engine, ensure_car_columns
from app.models import Car
Base.metadata.create_all(bind=engine)
ensure_car_columns()
cars = [
    Car(id=1, title='Тайота Камри 25', category='Авто', action='Продам', price=16500000, location='Алматы', description='Toyota Camry 25 американец, объем двигателя 3.5, в хорошем состоянии, возможно обмен на квартиру. Если дороже, то с моей стороны доплата. Срочно!!!', tags=['#Продам', '#Продаммашину', '#Срочно', '#ToyotaCamry', '#ToyotaCamry25', '#Черная'], image='/src/assets/images/camryblack.svg', detailimg='/src/assets/images/camryblack.svg', name='Арман', avatar='/src/assets/icons/avatar.svg', date='8 декабря 2022 г.'),
    Car(id=2, title='Honda CR-V 2020', category='Авто', action='Продам', price=12800000, location='Астана', description='Honda CR-V 2020 года, пробег 45000 км, один хозяин, полная комплектация, панорамная крыша. Торг уместен при осмотре.', tags=['#Продам', '#Продаммашину', '#HondaCRV', '#Внедорожник', '#Белая'], image='/src/assets/images/hondawhite.jpeg', detailimg='/src/assets/images/hondawhite.jpeg', name='Данияр', avatar='/src/assets/icons/avatar.svg', date='15 января 2023 г.'),
    Car(id=3, title='Куплю Lexus RX 350', category='Авто', action='Куплю', price=20000000, location='Шымкент', description='Ищу Lexus RX 350 2018-2021 года, без пробега по России, максимальная комплектация. Наличный расчёт, готов к сделке сразу.', tags=['#Куплю', '#LexusRX', '#Внедорожник', '#Срочно'], image='/src/assets/images/lexuswhite.jpeg', detailimg='/src/assets/images/lexuswhite.jpeg', name='Руслан', avatar='/src/assets/icons/avatar.svg', date='20 апреля 2023 г.'),
    Car(id=4, title='Mercedes-Benz E200 2021', category='Авто', action='Продам', price=22500000, location='Алматы', description='Mercedes-Benz E200 2021 года, пробег 30000 км, один хозяин, полная сервисная история, гарантия от дилера ещё действует. Идеальное состояние, не битый, не крашен.', tags=['#Продам', '#Продаммашину', '#MercedesBenz', '#MercedesE200', '#Белый'], image='/src/assets/images/mersedes.webp', detailimg='/src/assets/images/mersedes.webp', name='Санжар', avatar='/src/assets/icons/avatar.svg', date='18 июня 2023 г.'),
]
with SessionLocal() as db:
    for car in cars:
        existing = db.get(Car, car.id)
        if existing is None:
            db.add(car)
        else:
            for field in ('title', 'category', 'action', 'price', 'location', 'description', 'image', 'detailimg', 'name', 'avatar', 'date', 'tags'):
                setattr(existing, field, getattr(car, field))
    db.commit()
print('Seed completed')
