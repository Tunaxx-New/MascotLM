from huggingface_hub import InferenceClient

from vision.ivision_language_model import IVisionLanguageModel


class HuggingFaceVisionLanguageModelService(IVisionLanguageModel):
    def __init__(self, api_key: str, model: str):
        self.client = InferenceClient(model, api_key=api_key)

    def execute(self, base64_image: str, username: str, formality: str, whoiam: str, todo: str) -> str:
        image_url = f"data:image/png;base64,{base64_image}"

        return self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                f"{whoiam}\n"
                                "Carefully examine the current context of user screen (provided image).\n"
                                "Read text from screenshot (provided image).\n"
                                f"{todo} based on its content (provided image).\n"
                                f"Answer {formality}.\n\n"
                                f"user: {username}\n"
                                "Address the user by name for attention in the begining, middle or end (user)'\n"
                                "**Respond ONLY with the result. Do NOT explain it. Do NOT include any analysis or reasoning.**\n"
                                "Mention in result something from image (provided image)\n"
                                "**Limit your response to no more than 300 characters.**\n"
                                "**Responsd with emotions in text**"
                            )
                        },
                    ],
                },
            ],
        ).choices[0].message.content
