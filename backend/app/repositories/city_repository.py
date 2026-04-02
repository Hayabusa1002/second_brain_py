from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.city import City


class CityRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[City]:
        return self.db.query(City).order_by(City.name.asc()).all()

    def get_by_id(self, city_id: UUID) -> Optional[City]:
        return self.db.query(City).filter(City.id == city_id).first()

    def get_by_name(self, name: str) -> Optional[City]:
        return self.db.query(City).filter(City.name.ilike(name.strip())).first()

    def add(self, data) -> City:
        city = City(
            name=data.name,
            state=getattr(data, "state", None),
            country=getattr(data, "country", None),
        )
        self.db.add(city)
        self.db.commit()
        self.db.refresh(city)
        return city

    def update(self, city_id: UUID, data) -> Optional[City]:
        city = self.get_by_id(city_id)
        if not city:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(city, field, value)

        self.db.commit()
        self.db.refresh(city)
        return city