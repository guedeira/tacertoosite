from urllib.parse import urlsplit

import tldextract


class DomainNormalizerService:
    _extractor = tldextract.TLDExtract(cache_dir=None, suffix_list_urls=())
    _allowed_public_suffix_domains = {"gov.br"}

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

    def is_valid_submitted_link(self, value: str | None) -> bool:
        if value is None:
            return False

        cleaned_value = value.strip()
        if not cleaned_value or any(character.isspace() for character in cleaned_value):
            return False

        parsed = urlsplit(self._with_scheme(cleaned_value))
        if parsed.scheme and parsed.scheme not in {"http", "https"}:
            return False
        if parsed.username or parsed.password:
            return False

        try:
            parsed.port
        except ValueError:
            return False

        normalized_domain = self.normalize(cleaned_value)

        return self.is_valid_domain(normalized_domain) and self._has_known_public_suffix(normalized_domain)

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
        allowed_public_suffix_domain = self._allowed_public_suffix_domain_for(domain)
        if allowed_public_suffix_domain:
            return allowed_public_suffix_domain

        extracted = self._extractor(domain)
        return extracted.top_domain_under_public_suffix or domain

    def _has_known_public_suffix(self, domain: str) -> bool:
        extracted = self._extractor(domain)
        if extracted.top_domain_under_public_suffix:
            return True

        return bool(extracted.suffix) and domain in self._allowed_public_suffix_domains

    def _allowed_public_suffix_domain_for(self, domain: str) -> str | None:
        return next(
            (
                allowed_domain
                for allowed_domain in self._allowed_public_suffix_domains
                if domain == allowed_domain or domain.endswith(f".{allowed_domain}")
            ),
            None,
        )
