from urllib.parse import urlsplit

import tldextract


class DomainNormalizerService:
    _extractor = tldextract.TLDExtract(cache_dir=None, suffix_list_urls=())

    def normalize(self, value: str | None) -> str:
        if value is None:
            return ""

        cleaned_value = value.strip().lower()
        if not cleaned_value:
            return ""

        parsed = urlsplit(self._with_scheme(cleaned_value))
        domain = parsed.hostname or ""

        # Some official domains in the base, such as gov.br, are public suffixes.
        # tldextract keeps "www" in those cases, so strip that conventional prefix first.
        if domain.startswith("www."):
            domain = domain[4:]

        return self._registrable_domain(domain.rstrip("."))

    def is_valid_domain(self, domain: str) -> bool:
        if not domain or len(domain) > 253:
            return False

        labels = domain.split(".")
        if len(labels) < 2:
            return False

        return all(self._is_valid_label(label) for label in labels)

    def _with_scheme(self, value: str) -> str:
        if "://" in value:
            return value
        return f"//{value}"

    def _is_valid_label(self, label: str) -> bool:
        if not label or len(label) > 63:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        return all(character.isalnum() or character == "-" for character in label)

    def _registrable_domain(self, domain: str) -> str:
        extracted = self._extractor(domain)
        return extracted.top_domain_under_public_suffix or domain
