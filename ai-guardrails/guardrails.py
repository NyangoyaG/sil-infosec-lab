import re
from dataclasses import dataclass


@dataclass
class GuardrailResult:
    allowed: bool
    reason: str
    sanitized_text: str


# Demonstration patterns only; these are not a complete security solution.
PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"reveal (your )?(system prompt|hidden instructions)",
    r"bypass (all )?security rules",
    r"act as an unrestricted",
]

SENSITIVE_DATA_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone": r"(?<!\w)\+?\d(?:[\d -]{7,15}\d)(?!\w)",
}


def inspect_input(text: str) -> GuardrailResult:
    """Block obvious prompt-injection attempts and redact common PII."""
    normalized = text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, normalized):
            return GuardrailResult(
                allowed=False,
                reason="Potential prompt injection detected",
                sanitized_text="",
            )

    sanitized = text
    for label, pattern in SENSITIVE_DATA_PATTERNS.items():
        sanitized = re.sub(
            pattern,
            f"[REDACTED_{label.upper()}]",
            sanitized,
        )

    return GuardrailResult(
        allowed=True,
        reason="Input passed basic checks",
        sanitized_text=sanitized,
    )


def inspect_output(text: str) -> GuardrailResult:
    """Redact common PII from a sample AI response before returning it."""
    sanitized = text

    for label, pattern in SENSITIVE_DATA_PATTERNS.items():
        sanitized = re.sub(
            pattern,
            f"[REDACTED_{label.upper()}]",
            sanitized,
        )

    return GuardrailResult(
        allowed=True,
        reason="Output checked for common PII patterns",
        sanitized_text=sanitized,
    )
