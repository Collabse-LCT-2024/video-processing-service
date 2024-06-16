import torch
import whisper


class WhisperTranscriber:
    def __init__(self, model_name="medium"):
        self.model_name = model_name
        self.model = whisper.load_model(model_name, in_memory=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)

    def transcribe(self, audio_path):
        try:
            result = self.model.transcribe(audio_path, condition_on_previous_text=False, no_speech_threshold=0.2)
            return result
        except Exception:
            raise Exception("Failed to transcribe audio")

    @staticmethod
    def get_language(result):
        return result["language"]

    @staticmethod
    def get_text(result):
        return result["text"]
