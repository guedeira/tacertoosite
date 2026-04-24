from app.models.brand import Brand
from app.repositories.brand_repository import BrandRepository


class BrandService:
    def __init__(self, repository: BrandRepository | None = None) -> None:
        self.repository = repository or BrandRepository()

    def list_brands(self) -> list[Brand]:
        return self.repository.list_all()

    def get_brand(self, brand_id: str) -> Brand | None:
        return self.repository.get_by_id(brand_id)
