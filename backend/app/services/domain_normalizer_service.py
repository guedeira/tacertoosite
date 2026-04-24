from urllib.parse import urlsplit


class DomainNormalizerService:
    def normalize(self, value: str | None) -> str:
        if value is None:
            return ""

        cleaned_value = value.strip().lower()
        if not cleaned_value:
            return ""

        parsed = urlsplit(self._with_scheme(cleaned_value))
        domain = parsed.hostname or ""

        if domain.startswith("www."):
            domain = domain[4:]

        return domain.rstrip(".")

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
