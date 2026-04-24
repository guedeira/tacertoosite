from app.services.brand_service import BrandService


class BrandController:
    def __init__(self, service: BrandService | None = None) -> None:
        self.service = service or BrandService()

    def list_brands(self) -> list[dict]:
        return [brand.to_dict() for brand in self.service.list_brands()]

    def get_brand(self, brand_id: str) -> dict | None:
        brand = self.service.get_brand(brand_id)
        if brand is None:
            return None
        return brand.to_dict()
