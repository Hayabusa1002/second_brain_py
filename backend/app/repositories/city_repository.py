from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_
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

    def get_by_identity(
        self,
        name: str,
        state: str | None = None,
        country: str | None = None,
    ) -> Optional[City]:
        query = self.db.query(City).filter(City.name.ilike(name.strip()))

        if state is None or not str(state).strip():
            query = query.filter(or_(City.state.is_(None), City.state == ""))
        else:
            query = query.filter(City.state.ilike(str(state).strip()))

        if country is None or not str(country).strip():
            query = query.filter(or_(City.country.is_(None), City.country == ""))
        else:
            query = query.filter(City.country.ilike(str(country).strip()))

        return query.first()

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

    def add_from_values(
        self,
        name: str,
        state: str | None = None,
        country: str | None = None,
    ) -> City:
        city = City(
            name=name,
            state=state,
            country=country,
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

    def delete(self, city_id: UUID) -> bool:
        city = self.get_by_id(city_id)
        if not city:
            return False

        self.db.delete(city)
        self.db.commit()
        return True