import os
import random
from researcher import Researcher
from script_writer import ScriptWriter
from voice_generator import VoiceGenerator
from visuals_generator import VisualsGenerator
from video_editor import VideoEditor
from uploader import YouTubeUploader
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=== YouTube Automation System Started ===")
    
    # Check if necessary API keys exist
    if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "your_openrouter_api_key_here":
        print("ERROR: Please set your OPENROUTER_API_KEY in the .env file.")
        return

    # 1. Topic Research
    print("\n[1] Starting Topic Research...")
    researcher = Researcher()
    # Force programming niche for Java Interview Questions video
    niche = "programming"
    topic = "Top Java Interview Questions You Must Know"
    print(f"Selected Niche: {niche}")
    print(f"Selected Topic: {topic}")

    # 2. Script Generation
    print("\n[2] Generating Script...")
    script_writer = ScriptWriter()
    script = script_writer.generate_script(topic, target_length_minutes=2)
    if not script:
        print("Failed to generate script. Exiting.")
        return
    print("Script successfully generated!")

    # 3. Voice Generation
    print("\n[3] Generating Voiceover...")
    voice_generator = VoiceGenerator()
    audio_path = voice_generator.generate_voice(script)
    if not audio_path:
        print("Failed to generate voice. Exiting.")
        return

    # 4. Visuals Generation
    print("\n[4] Generating B-Roll...")
    # Very simple keyword extraction: just the first 3 words of the topic, or we can use OpenAI to extract search queries
    # For MVP, we'll try to find visuals matching the exact topic or split it
    query = topic.split()[0] if len(topic.split()) > 0 else "technology"
    print(f"Using query '{query}' for B-roll search...")
    
    visuals_generator = VisualsGenerator()
    b_roll_paths = visuals_generator.generate_b_roll_for_query(query, count=6)
    if not b_roll_paths:
        print(f"Failed to find B-Roll clips for query '{query}'. Exiting.")
        return

    # 5. Video Editor Assembly
    print("\n[5] Assembling Final Video...")
    video_editor = VideoEditor()
    final_video_path = video_editor.create_video(audio_path, b_roll_paths)
    if not final_video_path:
        print("Failed to assemble video. Exiting.")
        return

    # 6. YouTube Upload
    print("\n[6] Initializing YouTube Upload...")
    uploader = YouTubeUploader()
    # If the user hasn't set up credentials, this will pause and ask.
    # In a fully headless cron job, token.json must already be generated once manually.
    
    title = f"{topic} | {niche.replace('_', ' ').title()}"
    description = f"Watch this amazing breakdown on {topic}. Leave a comment if you enjoyed it! \n\n#shorts #{niche.replace('_', '')}"
    tags = [niche, query, "video", "educational", "story", "documentary"]

    video_id = uploader.upload_video(
        video_path=final_video_path,
        title=title,
        description=description,
        tags=tags,
        privacy_status="private" # Start with private to review the results safely
    )

    if video_id:
        print(f"\n=== SUCCESS! Video uploaded: https://youtube.com/watch?v={video_id} ===")
    else:
        print("\n=== Upload failed, but video was rendered locally. ===")

if __name__ == "__main__":
    main()
