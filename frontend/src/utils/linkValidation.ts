import { z } from "zod";
import { parse } from "tldts";

export const SUBMITTED_LINK_MAX_LENGTH = 2048;
const ALLOWED_PUBLIC_SUFFIX_DOMAINS = new Set(["gov.br"]);

export const submittedLinkSchema = z
  .string()
  .trim()
  .min(1, "Digite um link válido.")
  .max(SUBMITTED_LINK_MAX_LENGTH, "O link está muito longo.")
  .refine(isValidSubmittedLink, "Digite um link válido.");

export function isValidSubmittedLink(value: string): boolean {
  const trimmedValue = value.trim();

  if (!trimmedValue || /\s/.test(trimmedValue)) {
    return false;
  }

  const hasScheme = /^[a-z][a-z0-9+.-]*:\/\//i.test(trimmedValue);

  let url: URL;
  try {
    url = new URL(hasScheme ? trimmedValue : `https://${trimmedValue}`);
  } catch {
    return false;
  }

  if (!["http:", "https:"].includes(url.protocol)) {
    return false;
  }

  if (url.username || url.password) {
    return false;
  }

  const hostname = url.hostname.toLowerCase().replace(/\.$/, "");

  return isValidDomain(hostname) && hasKnownPublicSuffix(hostname);
}

function isValidDomain(domain: string): boolean {
  if (!domain || domain.length > 253) {
    return false;
  }

  const labels = domain.split(".");

  if (labels.length < 2) {
    return false;
  }

  return labels.every((label) => /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(label));
}

function hasKnownPublicSuffix(hostname: string): boolean {
  const parsed = parse(hostname);

  if (parsed.isIcann && parsed.domain) {
    return true;
  }

  return Boolean(parsed.isIcann && parsed.publicSuffix && ALLOWED_PUBLIC_SUFFIX_DOMAINS.has(hostname.replace(/^www\./, "")));
}
