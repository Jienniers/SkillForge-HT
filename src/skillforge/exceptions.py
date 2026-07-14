"""Application-specific errors."""


class SkillForgeError(Exception):
    """Base error for expected application failures."""


class ConfigurationError(SkillForgeError):
    """Raised when required runtime configuration is absent."""


class GenerationError(SkillForgeError):
    """Raised when an AI response cannot be used safely."""


class InvalidRoadmapError(SkillForgeError):
    """Raised when the local roadmap file has an unexpected shape."""
