import os
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

class VoiceGenerator:
    def __init__(self):
        print("Voice generator initialized (using gTTS - free Google TTS).")

    def generate_voice(self, text: str, output_path: str = "assets/audio/voiceover.mp3") -> str:
        """
        Takes a script and creates an MP3 using Google Text-to-Speech (gTTS).
        Free, no API key or credits required.
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)

            print(f"Voiceover saved to: {output_path}")
            return output_path

        except Exception as e:
            print(f"Error generating voice: {str(e)}")
            return ""

if __name__ == "__main__":
    generator = VoiceGenerator()
    sample_text = "Welcome to our channel. Today, we are discussing the incredible story of Elon Musk."
    print("Generating sample voiceover...")
    output = generator.generate_voice(sample_text, "assets/audio/sample_voiceover.mp3")
    if output:
        print(f"Saved to: {output}")
