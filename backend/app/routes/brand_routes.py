from fastapi import APIRouter, HTTPException

from app.controllers.brand_controller import BrandController

router = APIRouter()
controller = BrandController()


@router.get("/brands")
def list_brands() -> list[dict]:
    return controller.list_brands()


@router.get("/brands/{brand_id}")
def get_brand(brand_id: str) -> dict:
    brand = controller.get_brand(brand_id)
    if brand is None:
        raise HTTPException(status_code=404, detail="Marca não encontrada.")
    return brand
