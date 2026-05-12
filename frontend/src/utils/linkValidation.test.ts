import { describe, expect, it } from "vitest";

import { isValidSubmittedLink, submittedLinkSchema } from "./linkValidation";

describe("link validation utilities", () => {
  it("accepts full https links", () => {
    expect(isValidSubmittedLink("https://www.nubank.com.br/app")).toBe(true);
  });

  it("accepts domains without scheme", () => {
    expect(isValidSubmittedLink("nubank.com.br")).toBe(true);
  });

  it("rejects plain text without a public suffix", () => {
    expect(isValidSubmittedLink("nubank")).toBe(false);
  });

  it("rejects domains with unknown public suffixes", () => {
    expect(isValidSubmittedLink("sdfsd.fdsfds.fdsfdsf.sfsdfdsf.dsfds")).toBe(false);
  });

  it("rejects links with raw spaces", () => {
    expect(isValidSubmittedLink("https://nubank.com.br/minha conta")).toBe(false);
  });

  it("rejects links with credentials", () => {
    expect(isValidSubmittedLink("https://user:pass@nubank.com.br")).toBe(false);
  });

  it("returns the trimmed link from the schema", () => {
    expect(submittedLinkSchema.parse(" https://nubank.com.br/app ")).toBe("https://nubank.com.br/app");
  });

  it("accepts allowed public suffix domains", () => {
    expect(isValidSubmittedLink("https://www.gov.br/servicos")).toBe(true);
  });
});
