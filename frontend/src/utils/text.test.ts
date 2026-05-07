import { describe, expect, it } from "vitest";

import { filterCompanies, normalizeText } from "./text";

describe("text utilities", () => {
  it("normalizes accents, case and whitespace", () => {
    expect(normalizeText("  Magazine Luíza  ")).toBe("magazine luiza");
  });

  it("filters companies by normalized name", () => {
    const companies = [
      { id: "mercado_livre", name: "Mercado Livre" },
      { id: "magazine_luiza", name: "Magazine Luiza" },
    ];

    expect(filterCompanies(companies, "luiza")).toEqual([{ id: "magazine_luiza", name: "Magazine Luiza" }]);
  });
});
