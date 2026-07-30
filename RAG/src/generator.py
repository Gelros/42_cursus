"""Qwen3-0.6B wrapper for answer generation.

This is the same QwenGenerator as in exercise 10 — instantiate once,
call answer() many times. Cold start ~10 s on cached model.
"""

from typing import cast

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class QwenGenerator:
    """Wrap Qwen3-0.6B with a tiny, RAG-friendly answer() API."""

    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B"):
        self.device = self.pick_device()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        dtype = torch.bfloat16 if self.device != "cpu" else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=dtype, device_map=self.device,
        )
        self.model.eval()

    @staticmethod
    def pick_device() -> str:
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def build_prompt(self, question: str, context: str) -> str:
        """Apply Qwen's ChatML template with a strict system prompt."""
        messages = [
            {
                "role": "system",
                "content": (
                    "Answer the question using ONLY the provided context. "
                    "Be concise. If the answer is not in the context, say "
                    "you don't know."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ]
        # tokenize=False guarantees a str; cast narrows the library's union.
        # enable_thinking=False: Qwen3 is a reasoning model; we want a direct,
        # concise answer (subject V.2.3) without the <think>...</think> block.
        return cast(
            str,
            self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            ),
        )

    def answer(
        self,
        question: str,
        context: str,
        max_new_tokens: int = 128,
    ) -> str:
        """Generate a deterministic answer from question + context."""
        prompt = self.build_prompt(question, context)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            # transformers types `.generate` loosely on the auto-loaded model.
            out = self.model.generate(  # type: ignore[misc]
                **inputs, max_new_tokens=max_new_tokens, do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        prompt_length = inputs["input_ids"].shape[1]
        answer_ids = out[0, prompt_length:]
        decoded = cast(
            str,
            self.tokenizer.decode(answer_ids, skip_special_tokens=True),
        )
        return decoded.strip()
