import os
import argparse
from researcher import Researcher
from script_writer import ScriptWriter
from voice_generator import VoiceGenerator
from visuals_generator import VisualsGenerator
from video_editor import VideoEditor
from uploader import YouTubeUploader
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="YouTube Automation Bot")
    parser.add_argument("--mode", type=str, choices=["long_form", "motivational_shorts"], default="long_form", 
                        help="Choose which type of video to generate (long_form or motivational_shorts)")
    parser.add_argument("--dry-run", action="store_true", help="Run without hitting APIs or rendering video (for testing)")
    args = parser.parse_args()

    print("=== YouTube Automation System Started ===")
    print(f"Mode: {args.mode}")

    if not args.dry_run:
        if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "your_openrouter_api_key_here":
            print("ERROR: Please set your OPENROUTER_API_KEY in the .env file.")
            return

    # Initialize Modules
    researcher = Researcher()
    script_writer = ScriptWriter()
    voice_generator = VoiceGenerator()
    visuals_generator = VisualsGenerator()
    video_editor = VideoEditor()
    uploader = YouTubeUploader()

    if args.mode == "motivational_shorts":
        # === MOTIVATIONAL SHORTS PIPELINE ===
        print("\n[1] Starting Shorts Topic Research...")
        niche = "motivational_stories"
        # We assume the researcher now has a dedicated shorts list, or we just pull from the niche
        topic = researcher.get_topic_for_niche(niche) 
        print(f"Selected Topic: {topic}")

        print("\n[2] Generating Shorts Script...")
        if args.dry_run:
            script = "This is a dry-run test script. You are closer than you think. Keep pushing."
            print(f"Dry run script: {script}")
        else:
            script = script_writer.generate_shorts_script(topic)
            if not script:
                print("Failed to generate shorts script. Exiting.")
                return
            print("Script successfully generated!")

        print("\n[3] Generating Voiceover...")
        if args.dry_run:
            audio_path = "assets/audio/dummy.mp3"
            print("Skipped voice generation for dry-run.")
        else:
            audio_path = voice_generator.generate_voice(script, "assets/audio/shorts_voiceover.mp3")
            if not audio_path:
                print("Failed to generate voice. Exiting.")
                return

        print("\n[4] Generating Portrait B-Roll...")
        query = topic.split()[0] if len(topic.split()) > 0 else "motivation"
        print(f"Using query '{query}' for B-roll search...")
        if args.dry_run:
            b_roll_paths = ["assets/video/dummy1.mp4"]
            print("Skipped Pexels download for dry-run.")
        else:
            b_roll_paths = visuals_generator.generate_shorts_b_roll(query, output_dir="assets/video/shorts", count=3)
            if not b_roll_paths:
                print(f"Failed to find B-Roll clips for query '{query}'. Exiting.")
                return

        print("\n[5] Assembling Shorts Video...")
        if args.dry_run:
            final_video_path = "assets/output/shorts_dummy.mp4"
            print("Skipped video rendering for dry-run.")
        else:
            final_video_path = video_editor.create_shorts_video(audio_path, b_roll_paths, quote_text=topic)
            if not final_video_path:
                print("Failed to assemble video. Exiting.")
                return

        print("\n[6] Initializing YouTube Upload...")
        if args.dry_run:
            print("Skipped YouTube upload for dry-run. Pipeline successful!")
            return
            
        title = f"{topic} #shorts #motivation"
        description = f"Watch this quick motivational hit on {topic}. Leave a comment if this resonated with you! \n\n#shorts #motivation #mindset"
        tags = ["motivation", "shorts", "mindset", "success", "inspiration", query]

        video_id = uploader.upload_video(
            video_path=final_video_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status="private"
        )

        if video_id:
            print(f"\n=== SUCCESS! Short uploaded: https://youtube.com/watch?v={video_id} ===")
        else:
            print("\n=== Upload failed, but video was rendered locally. ===")

    else:
        # === LONG FORM PIPELINE ===
        print("\n[1] Starting Topic Research...")
        niche = "programming"
        topic = "Top Java Interview Questions You Must Know"
        print(f"Selected Niche: {niche}")
        print(f"Selected Topic: {topic}")

        print("\n[2] Generating Script...")
        if args.dry_run:
            print("Skipping real API call for dry-run.")
            return
            
        script = script_writer.generate_script(topic, target_length_minutes=2)
        if not script:
            print("Failed to generate script. Exiting.")
            return
        print("Script successfully generated!")

        print("\n[3] Generating Voiceover...")
        audio_path = voice_generator.generate_voice(script)
        if not audio_path:
            return

        print("\n[4] Generating B-Roll...")
        query = topic.split()[0] if len(topic.split()) > 0 else "technology"
        b_roll_paths = visuals_generator.generate_b_roll_for_query(query, count=6)
        if not b_roll_paths:
            return

        print("\n[5] Assembling Final Video...")
        final_video_path = video_editor.create_video(audio_path, b_roll_paths)
        if not final_video_path:
            return

        print("\n[6] Initializing YouTube Upload...")
        title = f"{topic} | {niche.replace('_', ' ').title()}"
        description = f"Watch this amazing breakdown on {topic}.\n\n#programming"
        tags = [niche, query, "video", "educational"]

        video_id = uploader.upload_video(
            video_path=final_video_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status="private"
        )
        if video_id:
            print(f"\n=== SUCCESS! Video uploaded: https://youtube.com/watch?v={video_id} ===")
        else:
            print("\n=== Upload failed, but video was rendered locally. ===")

if __name__ == "__main__":
    main()
