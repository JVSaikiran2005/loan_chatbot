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
        # Prefer an instruction-following model by default to reduce hallucinations
        self.model_name = model_name or os.getenv(
            "HF_LOAN_MODEL_NAME", "google/flan-t5-small"
        )
        self.max_new_tokens = max_new_tokens

        self._generator = None

        # Initialize a text-generation pipeline if the transformers
        # library is available and working. If anything goes wrong,
        # we fall back gracefully so that the main app still runs.
        if pipeline is not None:
            try:
                # Choose pipeline task based on model type (seq2seq instruction models vs. causal LM)
                model_lower = (self.model_name or '').lower()
                if 'flan' in model_lower or 't5' in model_lower or 'text2' in model_lower:
                    task = 'text2text-generation'
                else:
                    task = 'text-generation'

                # Initialize selected pipeline on CPU by default
                self._task = task
                self._generator = pipeline(
                    task,
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
            "Speak politely, professionally and clearly. Keep replies to one or two concise sentences. "
            "Answer only about loans, eligibility, documents, credit checks, and the loan process. "
            "Do not invent personal history or make unverifiable claims. Do not provide legal or financial advice beyond general information. "
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
            # Use different generation kwargs depending on pipeline task
            task = getattr(self, '_task', 'text-generation')
            if task == 'text2text-generation':
                gen_kwargs = dict(
                    max_new_tokens=min(self.max_new_tokens, 64),
                    do_sample=False,
                    num_return_sequences=1,
                )
            else:
                gen_kwargs = dict(
                    max_new_tokens=min(self.max_new_tokens, 64),
                    do_sample=False,
                    num_return_sequences=1,
                    repetition_penalty=1.2,
                )

            outputs = self._generator(prompt, **gen_kwargs)

            # Defensive checks around the Hugging Face output structure
            if not outputs or not isinstance(outputs, list):
                raise ValueError("Unexpected model output format")

            first = outputs[0]
            if not isinstance(first, dict) or "generated_text" not in first:
                raise ValueError("Missing 'generated_text' in model output")

            raw = str(first["generated_text"])

            # Extract assistant reply and defensively trim repeated phrases.
            if "Assistant:" in raw:
                response_text = raw.split("Assistant:")[-1].strip()
            else:
                response_text = raw.strip()

            # Remove obvious repeated sentences (simple heuristic)
            parts = [p.strip() for p in response_text.split('.') if p.strip()]
            dedup = []
            for p in parts:
                if not dedup or p != dedup[-1]:
                    dedup.append(p)

            if dedup:
                response_text = '. '.join(dedup)
                if not response_text.endswith('.'):
                    response_text += '.'

            # Finally, enforce a short reply: keep only the first two sentences to avoid verbosity
            sentences = [s.strip() for s in response_text.split('.') if s.strip()]
            if len(sentences) > 2:
                response_text = '. '.join(sentences[:2]) + '.'

            # Basic safety: avoid returning an empty string
            if not response_text:
                response_text = (
                    "I'm here to help you with personal loans, eligibility and required documents. "
                    "Could you please rephrase your question?"
                )

            # Simple content filter: if model claims personal attributes or clearly off-topic text, fallback
            low = response_text.lower()
            off_topic_markers = ['i am in my', 'i have a degree', 'my first experience', 'we were young', 'paypal']
            if any(marker in low for marker in off_topic_markers):
                return (
                    "I'm currently unable to provide a detailed ML-generated reply. "
                    "I can still guide you through the loan process and required documents."
                )

            return response_text

        except Exception:
            # Absolute last-resort fallback: never let an ML error crash the app.
            return (
                "I'm having trouble generating a smart response right now, "
                "but I can still help you with loan eligibility, documents and application steps. "
                "Please tell me what you would like to know."
            )

