"""Domain exceptions. cli.py turns them into `error: ...` lines, like a Spring @ControllerAdvice."""


class PetClinicError(Exception):
    """Base class for expected, user-facing errors."""


class NotFoundError(PetClinicError):
    """No entity with the given id exists. The HTTP equivalent is 404."""


class ValidationError(PetClinicError):
    """The input breaks a business rule. The HTTP equivalent is 400."""
