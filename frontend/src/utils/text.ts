export function normalizeText(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

export function filterBrands<T extends { name: string }>(brands: T[], term: string, limit = 6): T[] {
  const normalizedTerm = normalizeText(term);

  if (!normalizedTerm) {
    return [];
  }

  return brands
    .filter((brand) => normalizeText(brand.name).includes(normalizedTerm))
    .slice(0, limit);
}
