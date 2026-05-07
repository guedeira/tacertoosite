import { beforeEach, describe, expect, it, vi } from "vitest";

import { getCompanies, validateDomain } from "./api";

describe("api service", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  it("loads companies from the API", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify([{ id: "google", name: "Google" }]), { status: 200 }));

    await expect(getCompanies()).resolves.toEqual([{ id: "google", name: "Google" }]);
  });

  it("posts validation payload", async () => {
    const response = {
      is_match: true,
      company: "Google",
      official_domains: ["google.com"],
      submitted_domain: "google.com",
      message: "Domínio encontrado.",
    };

    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify(response), { status: 200 }));

    await expect(validateDomain({ company_id: "google", input: "https://google.com" })).resolves.toEqual(response);
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/validate-domain"),
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ company_id: "google", input: "https://google.com" }),
      }),
    );
  });
});
