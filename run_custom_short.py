import os
from voice_generator import VoiceGenerator
from visuals_generator import VisualsGenerator
from video_editor import VideoEditor
from uploader import YouTubeUploader
from dotenv import load_dotenv

load_dotenv()

def run_clone():
    print("=== YouTube Clone Generation Started ===")
    
    # Translated and polished script from the Hindi transcript
    script = (
        "What is the one feature of Java that makes it completely platform independent? "
        "Welcome to Day One of the 100 Days, 100 Interview Questions series! "
        "The code that we write as developers is called source code. Once we finish writing "
        "our code, we compile it using the Java compiler, also known as javac. Once the code is "
        "compiled, the Java compiler generates something called Bytecode! This Bytecode is the "
        "most important piece of the puzzle. It is the exact code that makes Java platform independent! "
        "Once the Bytecode is generated, we can take it and run it on absolutely any hardware. "
        "Whether it's a Mac, Windows, or Linux machine, Java runs everywhere!"
    )
    topic = "What Makes Java Platform Independent?"
    query = "programming code" # for b-roll

    print("\n[1] Generating Voiceover...")
    voice_generator = VoiceGenerator()
    audio_path = voice_generator.generate_voice(script, "assets/audio/clone_voiceover2.mp3")
    if not audio_path:
        print("Failed to generate voice. Exiting.")
        return

    print("\n[2] Generating Portrait B-Roll...")
    visuals_generator = VisualsGenerator()
    b_roll_paths = visuals_generator.generate_shorts_b_roll(query, output_dir="assets/video/clone2", count=4)
    if not b_roll_paths:
        print(f"Failed to find B-Roll clips for query '{query}'. Exiting.")
        return

    print("\n[3] Assembling Clone Video...")
    video_editor = VideoEditor()
    # Add a custom quote overlay for the video
    final_video_path = video_editor.create_shorts_video(audio_path, b_roll_paths, quote_text="Java Bytecode Explained", output_path="assets/output/clone_video2.mp4")
    if not final_video_path:
        print("Failed to assemble video. Exiting.")
        return

    print("\n[4] Initializing YouTube Upload...")
    uploader = YouTubeUploader()
            
    title = f"{topic} #shorts #java #programming"
    description = f"Understanding Java Bytecode and why Java is platform independent. Day 1 of 100 Days 100 Interview Questions! \n\n#shorts #java #coding #interview"
    tags = ["java", "shorts", "programming", "coding", "interview", "software"]

    video_id = uploader.upload_video(
        video_path=final_video_path,
        title=title,
        description=description,
        tags=tags,
        privacy_status="private"
    )

    if video_id:
        print(f"\n=== SUCCESS! Clone uploaded: https://youtube.com/watch?v={video_id} ===")
    else:
        print("\n=== Upload failed, but video was rendered locally. ===")

if __name__ == "__main__":
    run_clone()
