import json
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.controllers.city_controller import CityController
from app.db.deps import get_current_user, get_db
from app.repositories.city_repository import CityRepository
from app.routers.helpers.downloads import build_template_download
from app.routers.templates.cities import (
    TEMPLATE_CSV,
    TEMPLATE_JSON,
    TEMPLATE_YAML,
)
from app.schemas.bulk_import import ImportResult
from app.schemas.city import CityCreate, CityResponse, CityUpdate
from app.services.city_service import (
    CityNotFoundError,
    CityService,
    DuplicateCityError,
)
from app.services.helpers.import_service import UnsupportedImportFormatError


router = APIRouter(prefix="/cities")


def get_controller(db: Session = Depends(get_db)) -> CityController:
    repository = CityRepository(db)
    service = CityService(repository)
    return CityController(service)


# ---------- Import templates ----------

@router.get("/import/template/csv")
def download_cities_template_csv():
    return build_template_download(
        content=TEMPLATE_CSV,
        filename="cities_template.csv",
        media_type="text/csv",
    )


@router.get("/import/template/json")
def download_cities_template_json():
    return build_template_download(
        content=json.dumps(TEMPLATE_JSON, indent=2),
        filename="cities_template.json",
        media_type="application/json",
    )


@router.get("/import/template/yaml")
def download_cities_template_yaml():
    return build_template_download(
        content=TEMPLATE_YAML,
        filename="cities_template.yaml",
        media_type="application/x-yaml",
    )


# ---------- Import ----------

@router.post("/import", response_model=ImportResult)
async def import_cities(
    file: UploadFile = File(...),
    controller: CityController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return await controller.import_cities(file=file, current_user=user)
    except UnsupportedImportFormatError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------- Reads ----------

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
    try:
        return controller.get_city(city_id)
    except CityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------- Writes ----------

@router.post("", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(
    data: CityCreate,
    controller: CityController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.create_city(data=data, user_id=user.id)
    except DuplicateCityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{city_id}", response_model=CityResponse)
def update_city(
    city_id: UUID,
    data: CityUpdate,
    controller: CityController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.update_city(city_id=city_id, data=data, user_id=user.id)
    except CityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateCityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
    city_id: UUID,
    controller: CityController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        controller.delete_city(city_id=city_id, user_id=user.id)
        return
    except CityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))