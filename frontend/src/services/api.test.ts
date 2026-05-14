import { beforeEach, describe, expect, it, vi } from "vitest";

import { clearCompaniesCache, getCompanies, validateDomain } from "./api";

describe("api service", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
    clearCompaniesCache();
    vi.useRealTimers();
  });

  it("loads companies from the API", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify([{ id: "google", name: "Google" }]), { status: 200 }));

    await expect(getCompanies()).resolves.toEqual([{ id: "google", name: "Google" }]);
  });

  it("reuses cached companies for five minutes", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-05-14T12:00:00Z"));
    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify([{ id: "google", name: "Google" }]), { status: 200 }));

    await expect(getCompanies()).resolves.toEqual([{ id: "google", name: "Google" }]);
    await expect(getCompanies()).resolves.toEqual([{ id: "google", name: "Google" }]);

    expect(fetch).toHaveBeenCalledTimes(1);

    vi.setSystemTime(new Date("2026-05-14T12:05:01Z"));
    vi.mocked(fetch).mockResolvedValueOnce(new Response(JSON.stringify([{ id: "nubank", name: "Nubank" }]), { status: 200 }));

    await expect(getCompanies()).resolves.toEqual([{ id: "nubank", name: "Nubank" }]);
    expect(fetch).toHaveBeenCalledTimes(2);
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
