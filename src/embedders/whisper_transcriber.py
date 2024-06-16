import torch
import whisper


class WhisperTranscriber:
    def __init__(self, model_name="medium"):
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = whisper.load_model(model_name, device=self.device, in_memory=True)

    def transcribe(self, audio_path):
        try:
            result = self.model.transcribe(audio_path, condition_on_previous_text=False, no_speech_threshold=0.2)
            return result
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return None

    @staticmethod
    def get_language(result):
        return result["language"]

    @staticmethod
    def get_text(result):
        return result["text"]
