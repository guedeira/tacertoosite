import { describe, expect, it } from "vitest";

import { filterBrands, normalizeText } from "./text";

describe("text utilities", () => {
  it("normalizes accents, case and whitespace", () => {
    expect(normalizeText("  Magazine Luíza  ")).toBe("magazine luiza");
  });

  it("filters brands by normalized name", () => {
    const brands = [
      { id: "mercado_livre", name: "Mercado Livre" },
      { id: "magazine_luiza", name: "Magazine Luiza" },
    ];

    expect(filterBrands(brands, "luiza")).toEqual([{ id: "magazine_luiza", name: "Magazine Luiza" }]);
  });
});

