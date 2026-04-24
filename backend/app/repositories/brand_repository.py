import json
from pathlib import Path

from app.models.brand import Brand


class BrandRepository:
    def __init__(self, data_path: Path | None = None) -> None:
        self.data_path = data_path or Path(__file__).resolve().parents[1] / "data" / "brands.json"

    def list_all(self) -> list[Brand]:
        return [Brand.from_dict(item) for item in self._read_data()]

    def get_by_id(self, brand_id: str) -> Brand | None:
        return next((brand for brand in self.list_all() if brand.id == brand_id), None)

    def _read_data(self) -> list[dict]:
        with self.data_path.open(encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return [
            brand
            for brands_by_category in data.values()
            for brand in brands_by_category
        ]
