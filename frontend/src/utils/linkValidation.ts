import { z } from "zod";

export const SUBMITTED_LINK_MAX_LENGTH = 2048;

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

  return isValidDomain(hostname);
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
