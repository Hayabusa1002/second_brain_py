from typing import Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate


class CityRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self) -> list[City]:
        return (
            self.db.query(City)
            .order_by(City.name.asc())
            .all()
        )

    def get_by_id(self, city_id: UUID) -> Optional[City]:
        return (
            self.db.query(City)
            .filter(City.id == city_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[City]:
        return (
            self.db.query(City)
            .filter(City.name.ilike(name.strip()))
            .first()
        )

    def get_by_identity(self, name: str, state: str | None = None, country: str | None = None) -> Optional[City]:
        query = (
            self.db.query(City)
            .filter(City.name.ilike(name.strip()))
        )

        if state is None or not str(state).strip():
            query = query.filter(or_(City.state.is_(None), City.state == ""))
        else:
            query = query.filter(City.state.ilike(str(state).strip()))

        if country is None or not str(country).strip():
            query = query.filter(or_(City.country.is_(None), City.country == ""))
        else:
            query = query.filter(City.country.ilike(str(country).strip()))

        return query.first()

    # ---------- Writes ----------

    def create(self, data: CityCreate, user_id: UUID) -> City:
        city = City(
            name=data.name.strip(),
            state=data.state.strip() if data.state else None,
            country=data.country.strip() if data.country else None,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(city)
        self.db.commit()
        self.db.refresh(city)
        return self.get_by_id(city.id)

    def update(self, city_id: UUID, data: CityUpdate, user_id: UUID) -> Optional[City]:
        city = self.get_by_id(city_id)
        if not city:
            return None

        # exclude_unset avoids update as None the non-sended fields
        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()
            setattr(city, field, value)

        city.updated_by = user_id

        self.db.commit()
        self.db.refresh(city)
        return self.get_by_id(city.id)

    def delete(self, city_id: UUID) -> bool:
        city = self.get_by_id(city_id)
        if not city:
            return False

        self.db.delete(city)
        self.db.commit()
        return True