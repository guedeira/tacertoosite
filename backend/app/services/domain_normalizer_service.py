from urllib.parse import urlsplit

import tldextract


class DomainNormalizerService:
    _trusted_aggregate_domains = ["gov.br"]
    _extractor = tldextract.TLDExtract(
        cache_dir=None,
        suffix_list_urls=(),
        extra_suffixes=_trusted_aggregate_domains,
    )

    def extract_submitted_domain(self, value: str | None) -> str | None:
        hostname = self._submitted_hostname(value)
        if not hostname:
            return None

        domain = self._comparable_domain(hostname)
        if not self.is_valid_domain(domain):
            return None

        extracted = self._extractor(domain)
        if extracted.top_domain_under_public_suffix or domain in self._trusted_aggregate_domains:
            return domain

        return None

    def normalize(self, value: str | None) -> str:
        hostname = self._hostname(value)
        if not hostname:
            return ""

        return self._comparable_domain(hostname)

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

    def _hostname(self, value: str | None) -> str:
        if value is None:
            return ""

        cleaned_value = value.strip().lower()
        if not cleaned_value:
            return ""

        parsed = urlsplit(self._with_scheme(cleaned_value))
        return (parsed.hostname or "").rstrip(".")

    def _submitted_hostname(self, value: str | None) -> str:
        if value is None:
            return ""

        cleaned_value = value.strip()
        if not cleaned_value or any(character.isspace() for character in cleaned_value):
            return ""

        parsed = urlsplit(self._with_scheme(cleaned_value))
        if parsed.scheme and parsed.scheme not in {"http", "https"}:
            return ""
        if parsed.username or parsed.password:
            return ""

        try:
            parsed.port
        except ValueError:
            return ""

        return self._hostname(cleaned_value)

    def _is_valid_label(self, label: str) -> bool:
        if not label or len(label) > 63:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        return all(character.isalnum() or character == "-" for character in label)

    def _comparable_domain(self, hostname: str) -> str:
        domain = hostname[4:] if hostname.startswith("www.") else hostname

        trusted_domain = self._trusted_aggregate_domain_for(domain)
        if trusted_domain:
            return trusted_domain

        extracted = self._extractor(domain)
        return extracted.top_domain_under_public_suffix or domain

    def _trusted_aggregate_domain_for(self, domain: str) -> str | None:
        return next(
            (
                trusted_domain
                for trusted_domain in self._trusted_aggregate_domains
                if domain == trusted_domain or domain.endswith(f".{trusted_domain}")
            ),
            None,
        )
