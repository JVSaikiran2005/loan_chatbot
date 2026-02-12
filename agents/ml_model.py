import os
from typing import Any, Dict, Optional

try:
    # Heavy dependencies are imported lazily so that the main app
    # can still start even if transformers/torch are not installed
    # or correctly configured.
    from transformers import pipeline  # type: ignore
except Exception as e:  # pragma: no cover - defensive import
    pipeline = None  # type: ignore


class LoanChatModel:
    """
    Lightweight wrapper around a Hugging Face text-generation model
    for conversational responses in the loan assistant.

    By default this uses a small, publicly-available model so it can
    run locally without any external API keys.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        max_new_tokens: int = 128,
    ) -> None:
        # Allow overriding the model via environment variable.
        # Use a relatively small model by default to reduce download
        # size and memory usage.
        self.model_name = model_name or os.getenv(
            "HF_LOAN_MODEL_NAME", "distilgpt2"
        )
        self.max_new_tokens = max_new_tokens

        self._generator = None

        # Initialize a text-generation pipeline if the transformers
        # library is available and working. If anything goes wrong,
        # we fall back gracefully so that the main app still runs.
        if pipeline is not None:
            try:
                self._generator = pipeline(
                    "text-generation",
                    model=self.model_name,
                    device="cpu",
                )
            except Exception as e:  # pragma: no cover - runtime protection
                # In a real app we might want to log this to a file;
                # for now we just disable ML responses.
                self._generator = None

    def generate_response(
        self,
        user_message: str,
        conversation_data: Dict[str, Any],
    ) -> str:
        """
        Generate a conversational response for the given user message.

        This uses a simple prompt that conditions the model to behave
        like a banking loan assistant. The existing rule-based logic
        continues to handle the strict loan process; this model is
        primarily for more natural, free-form replies and fallbacks.
        """
        status = conversation_data.get("status", "initial")
        customer_name = conversation_data.get("customer_data", {}).get("name", "Customer")

        system_prompt = (
            "You are an AI banking assistant for a personal loan portal at Tata Capital. "
            "Speak politely, concisely and clearly. "
            "You can answer questions about personal loans, eligibility, documents, credit checks "
            "and the general loan process. "
            "Do not promise anything that contradicts the bank's policies. "
        )

        context = (
            f"Conversation status: {status}.\n"
            f"Customer name (if known): {customer_name}.\n"
        )

        prompt = (
            f"{system_prompt}\n"
            f"{context}\n"
            f"User: {user_message}\n"
            "Assistant:"
        )

        # If the generator is not available (e.g. transformers/torch
        # not installed correctly), fall back to a safe, static reply
        # so that the app never crashes.
        if self._generator is None:
            return (
                "I'm currently unable to use the ML model, but I can still guide you "
                "through the loan process. Please tell me what help you need with your loan."
            )

        try:
            outputs = self._generator(
                prompt,
                max_new_tokens=self.max_new_tokens,
                do_sample=True,
                top_p=0.92,
                temperature=0.7,
                num_return_sequences=1,
            )

            # Defensive checks around the Hugging Face output structure
            if not outputs or not isinstance(outputs, list):
                raise ValueError("Unexpected model output format")

            first = outputs[0]
            if not isinstance(first, dict) or "generated_text" not in first:
                raise ValueError("Missing 'generated_text' in model output")

            raw = str(first["generated_text"])

            # Try to return only the part after the last "Assistant:" marker
            if "Assistant:" in raw:
                response_text = raw.split("Assistant:")[-1].strip()
            else:
                response_text = raw.strip()

            # Basic safety: avoid returning an empty string
            if not response_text:
                response_text = (
                    "I'm here to help you with personal loans, eligibility and required documents. "
                    "Could you please rephrase your question?"
                )

            return response_text

        except Exception:
            # Absolute last-resort fallback: never let an ML error crash the app.
            return (
                "I'm having trouble generating a smart response right now, "
                "but I can still help you with loan eligibility, documents and application steps. "
                "Please tell me what you would like to know."
            )

