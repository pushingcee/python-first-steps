from petclinic.exceptions import ValidationError


def require_text(value: str, field_name: str) -> str:
    """Strip surrounding whitespace and reject blank values."""
    stripped = value.strip()
    if not stripped:
        raise ValidationError(f"{field_name} must not be blank")
    return stripped
