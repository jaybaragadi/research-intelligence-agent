from typing import Protocol

from src.generation.models import (
    EvidencePackage,
    GeneratedDraft,
)


class AnswerGenerator(
    Protocol,
):
    """
    Provider-independent answer-generation
    interface.

    Future implementations may use:

    - OpenAI
    - Claude
    - local models
    - another provider

    The rest of the system should not depend
    on a particular LLM SDK.
    """

    def generate(
        self,
        package: EvidencePackage,
    ) -> GeneratedDraft: ...
