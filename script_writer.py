import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ScriptWriter:
    def __init__(self):
        # Configure OpenRouter AI
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            print("WARNING: OPENROUTER_API_KEY is not set. Script generation will fail.")

    def generate_script(self, topic: str, target_length_minutes: int = 5) -> str:
        """
        Generates a YouTube script using OpenRouter (Free tier).
        """
        word_count_target = target_length_minutes * 150 # Roughly 150 words per minute for speaking
        
        prompt = f"""
        Write a highly engaging YouTube script for a faceless automation channel.
        Topic: {topic}
        Style: Storytelling, documentary style, fast-paced.
        Length: Approximately {word_count_target} words (aiming for a {target_length_minutes}-minute video).
        
        Requirements:
        1. Open with a compelling hook in the first 5 seconds to retain viewer attention.
        2. Keep paragraphs short and punchy.
        3. Do NOT include visual cues, staging directions, or music cues in brackets (e.g., no [Upbeat music playing], no [Cut to image of Tesla]). The output must be PURE spoken dialogue only.
        4. End with a strong call to action to subscribe and like the video.
        
        The script should start immediately with the spoken words of the hook.
        """

        try:
            # OpenRouter is 100% compatible with the OpenAI python SDK
            import openai
            client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
            response = client.chat.completions.create(
                model="liquid/lfm-2.5-1.2b-instruct:free",
                messages=[
                    {"role": "system", "content": "You are a top-tier YouTube scriptwriter who creates viral automated content."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating script: {str(e)}")
            return ""

    def generate_shorts_script(self, topic: str) -> str:
        """
        Generates a short, punchy motivational script (~120 words / ~45 seconds).
        """
        prompt = f"""
        Write a powerful, ultra-short motivational script for a YouTube Short.
        Topic: {topic}
        Style: Poetic, punchy, cinematic voiceover — like a movie trailer meets a motivational speech.
        Length: Exactly 110–130 words. No more. No less.

        Structure:
        1. ONE explosive hook sentence that grabs attention immediately.
        2. Three to four short, hard-hitting body lines — each a standalone punch.
        3. ONE unforgettable closing line that lingers in the mind.

        Rules:
        - No stage directions. No brackets. No [Music]. No [Cut to].
        - Pure spoken words only.
        - Every single word must earn its place.
        - Write in second person ("you", "your") to speak directly to the viewer.

        Start immediately with the hook. No preamble.
        """

        try:
            import openai
            client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
            response = client.chat.completions.create(
                model="liquid/lfm-2.5-1.2b-instruct:free",
                messages=[
                    {"role": "system", "content": "You are an elite motivational scriptwriter who crafts viral YouTube Shorts with cinematic, poetic voiceovers."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating shorts script: {str(e)}")
            return ""

if __name__ == "__main__":
    writer = ScriptWriter()
    sample_topic = "How Elon Musk Built Tesla"
    print(f"Generating sample script for: {sample_topic}...\n")
    script = writer.generate_script(sample_topic, target_length_minutes=1)
    if script:
        print(script)
    else:
        print("Failed to generate script.")

