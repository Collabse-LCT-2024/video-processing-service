from typing import List

from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image


class BlipEmbedder:
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-large", batch_size: int = 8):
        self.model = BlipForConditionalGeneration.from_pretrained(
            model_name, torch_dtype=torch.float16
        )
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)

        self.batch_size = batch_size

    @staticmethod
    def _open_images(image_paths: List[str]) -> List:
        return [Image.open(img_path) for img_path in image_paths]

    def embed(self, image_paths: List[str]) -> List:

        images = self._open_images(image_paths)

        result = []
        for batch in range(0, len(images), self.batch_size):
            raw_images_batch = images[batch: batch + self.batch_size]
            inputs = self.processor(raw_images_batch, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                out = self.model.generate(**inputs)
            result_batch = self.processor.decode(out[0], skip_special_tokens=True)
            result.append(result_batch)
        return result
