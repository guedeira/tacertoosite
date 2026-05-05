import { beforeEach, describe, expect, it, vi } from "vitest";

import { getBrands, validateDomain } from "./api";

describe("api service", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  it("loads brands from the API", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify([{ id: "google", name: "Google" }]), { status: 200 }));

    await expect(getBrands()).resolves.toEqual([{ id: "google", name: "Google" }]);
  });

  it("posts validation payload", async () => {
    const response = {
      is_match: true,
      brand: "Google",
      official_domains: ["google.com"],
      submitted_domain: "google.com",
      message: "Domínio encontrado.",
    };

    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify(response), { status: 200 }));

    await expect(validateDomain({ brand_id: "google", input: "https://google.com" })).resolves.toEqual(response);
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/validate-domain"),
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ brand_id: "google", input: "https://google.com" }),
      }),
    );
  });
});

