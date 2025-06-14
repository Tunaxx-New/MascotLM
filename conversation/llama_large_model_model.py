import torch
import torch_directml
from transformers import AutoTokenizer, AutoModelForCausalLM


class LlamaLargeModelModel:
    def __init__(self, model_name: str, cache_dir: str):
        self.model_name = model_name
        self.cache_dir = cache_dir

        # Fix missing attribute in some environments
        from transformers import modeling_utils
        if not hasattr(modeling_utils, "ALL_PARALLEL_STYLES") or modeling_utils.ALL_PARALLEL_STYLES is None:
            modeling_utils.ALL_PARALLEL_STYLES = ["tp", "none", "colwise", "rowwise"]

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, cache_dir=cache_dir, use_fast=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        self.device = torch_directml.device()
        self.model.to(self.device)

    def summarize_chunks(self, text: str, max_chunk_tokens: int = 960) -> str:
        # Tokenize the input text without special tokens
        tokens = self.tokenizer.encode(text, add_special_tokens=False)

        # Split tokens into chunks of max_chunk_tokens
        chunks = []
        for i in range(0, len(tokens), max_chunk_tokens):
            chunk_tokens = tokens[i:i + max_chunk_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)

        # Summarize each chunk individually
        return "\n".join([self._simple_summarize(chunk) for chunk in chunks])

    def _simple_summarize(self, chunk: str) -> str:
        prompt = f"Summarize the following:\n{chunk.strip()}"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(self.device)

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        print(output_ids[0])

        result = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return result.replace(prompt, "").strip()

    def generate_response(self, summary: str, username: str, formality: str, whoiam: str, todo: str) -> str:
        prompt_text = (
            f"You are a helpful assistant.\n"
            f"User: {username}\n"
            f"Formality: {formality}\n"
            f"Identity: {whoiam}\n"
            f"Task: {todo}\n"
            f"Summary: {summary}\n"
            f"Generate a suitable response for the user."
        )

        messages = [{"role": "user", "content": prompt_text}]
        try:
            prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        except Exception:
            prompt = prompt_text

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        result = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return result.replace(prompt, "").strip()

    def execute(self, text: str, username: str, formality: str, whoiam: str, todo: str) -> str:
        summary = self.summarize_chunks(text)
        return self.generate_response(summary, username, formality, whoiam, todo)
