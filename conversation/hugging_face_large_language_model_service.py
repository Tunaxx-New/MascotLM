from huggingface_hub import InferenceClient

from conversation.ilarge_language_model import ILargeLanguageModel


class HuggingFaceLargeLanguageModelService(ILargeLanguageModel):
    def __init__(self, api_key: str, model: str):
        self.client = InferenceClient(model, api_key=api_key)

    def execute(self, text: str, username: str, formality: str, whoiam: str, todo: str) -> str:
        return self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"content: {text}\n"
                                f"{whoiam}\n"
                                f"{todo} based on its content (provided content).\n"
                                f"Answer {formality}.\n\n"
                                f"user: {username}\n"
                                "Address the user by name for attention in the begining, middle or end (user)'\n"
                                "**Respond ONLY with the result. Do NOT explain it. Do NOT include any analysis or reasoning.**\n"
                                "Mention in result something from image (provided content)\n"
                                "**Limit your response to no more than 300 characters.**"
                                "**Responsd with emotions in text**"
                            )
                        },
                    ],
                },
            ],
        ).choices[0].message.content
