from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, require_admin
from app.controllers.city_controller import CityController
from app.services.city_service import CityService
from app.repositories.city_repository import CityRepository
from app.schemas.city import CityCreate, CityUpdate, CityResponse


router = APIRouter(
    prefix="/cities",
    tags=["cities"],
    dependencies=[Depends(require_admin)],
)


def get_controller(db: Session = Depends(get_db)) -> CityController:
    repository = CityRepository(db)
    service = CityService(repository)
    return CityController(service)


@router.get("/", response_model=List[CityResponse])
def list_cities(
    controller: CityController = Depends(get_controller),
):
    return controller.list_cities()


@router.get("/{city_id}", response_model=CityResponse)
def get_city(
    city_id: UUID,
    controller: CityController = Depends(get_controller),
):
    city = controller.get_city(city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/", response_model=CityResponse, status_code=201)
def create_city(
    data: CityCreate,
    controller: CityController = Depends(get_controller),
):
    return controller.create_city(data)


@router.patch("/{city_id}", response_model=CityResponse)
def update_city(
    city_id: UUID,
    data: CityUpdate,
    controller: CityController = Depends(get_controller),
):
    city = controller.update_city(city_id, data)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city