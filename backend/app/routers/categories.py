from fastapi import APIRouter

router = APIRouter()

categories = []

@router.post("/categories")
def create_category(category: dict):
    categories.append(category)
    return category

@router.get("/categories")
def list_categories():
    return categories