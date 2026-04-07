from typing import List
from uuid import UUID
import json

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.city_controller import CityController
from app.services.city_service import CityService
from app.repositories.city_repository import CityRepository
from app.schemas.city import CityCreate, CityUpdate, CityResponse
from app.schemas.bulk_import import ImportResult


router = APIRouter()


TEMPLATE_CSV = """name,state,country
Medellin,Antioquia,Colombia
Bogota,Cundinamarca,Colombia
Madrid,,Spain
Buenos Aires,,Argentina
"""


TEMPLATE_JSON = [
    {
        "name": "Medellin",
        "state": "Antioquia",
        "country": "Colombia",
    },
    {
        "name": "Bogota",
        "state": "Cundinamarca",
        "country": "Colombia",
    },
    {
        "name": "Madrid",
        "state": None,
        "country": "Spain",
    },
    {
        "name": "Buenos Aires",
        "state": None,
        "country": "Argentina",
    },
]


TEMPLATE_YAML = """- name: Medellin
  state: Antioquia
  country: Colombia

- name: Bogota
  state: Cundinamarca
  country: Colombia

- name: Madrid
  state:
  country: Spain

- name: Buenos Aires
  state:
  country: Argentina
"""


def get_controller(db: Session = Depends(get_db)) -> CityController:
    repository = CityRepository(db)
    service = CityService(repository)
    return CityController(service)


# --------- IMPORT TEMPLATES ---------


@router.get("/cities/import/template/csv", response_class=PlainTextResponse)
def download_cities_template_csv(
    current_user=Depends(get_current_user),
):
    return PlainTextResponse(
        content=TEMPLATE_CSV,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=cities_template.csv",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/cities/import/template/json")
def download_cities_template_json(
    current_user=Depends(get_current_user),
):
    return Response(
        content=json.dumps(TEMPLATE_JSON, indent=2),
        media_type="application/json",
        headers={
            "Content-Disposition": "attachment; filename=cities_template.json",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/cities/import/template/yaml", response_class=PlainTextResponse)
def download_cities_template_yaml(
    current_user=Depends(get_current_user),
):
    return PlainTextResponse(
        content=TEMPLATE_YAML,
        media_type="application/x-yaml",
        headers={
            "Content-Disposition": "attachment; filename=cities_template.yaml",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


# --------- IMPORT ---------


@router.post("/cities/import", response_model=ImportResult)
async def import_cities(
    file: UploadFile = File(...),
    controller: CityController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    if not file.filename or not any(
        file.filename.lower().endswith(ext)
        for ext in (".csv", ".xlsx", ".xls", ".json", ".yaml", ".yml")
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsupported format. Use CSV, XLSX, JSON or YAML.",
        )

    try:
        return await controller.import_cities(file, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------- CRUD ---------


@router.get("/cities", response_model=List[CityResponse])
def list_cities(
    controller: CityController = Depends(get_controller),
):
    return controller.list_cities()


@router.get("/cities/{city_id}", response_model=CityResponse)
def get_city(
    city_id: UUID,
    controller: CityController = Depends(get_controller),
):
    city = controller.get_city(city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities", response_model=CityResponse, status_code=201)
def create_city(
    data: CityCreate,
    controller: CityController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    return controller.create_city(data)


@router.patch("/cities/{city_id}", response_model=CityResponse)
def update_city(
    city_id: UUID,
    data: CityUpdate,
    controller: CityController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    city = controller.update_city(city_id, data)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
    city_id: UUID,
    controller: CityController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    deleted = controller.delete_city(city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return