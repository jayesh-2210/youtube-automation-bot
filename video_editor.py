from moviepy import VideoFileClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip
import os

class VideoEditor:
    def __init__(self):
        # We assume 1080x1920 (Shorts) or 1920x1080 (Landscape). 
        # Using 1920x1080 for standard long-form videos.
        self.resolution = (1920, 1080)
        
    def resize_clip(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Resizes and crops a clip to fit the target resolution.
        """
        from moviepy.video.fx import Resize, Crop
        
        # Crop and resize so video fills the screen
        clip = clip.with_effects([Resize(height=self.resolution[1])])
        if clip.w < self.resolution[0]:
            clip = clip.with_effects([Resize(width=self.resolution[0])])
            
        x_center = clip.w / 2
        y_center = clip.h / 2
        
        clip = clip.with_effects([Crop(
            x1=x_center - self.resolution[0]/2,
            y1=y_center - self.resolution[1]/2,
            x2=x_center + self.resolution[0]/2,
            y2=y_center + self.resolution[1]/2
        )])
        return clip

    def create_video(self, audio_path: str, b_roll_paths: list, output_path: str = "assets/output/final_video.mp4") -> str:
        """
        Concatenates b-roll clips and sets the provided audio.
        """
        try:
            print("Loading audio...")
            audio = AudioFileClip(audio_path)
            total_duration = audio.duration
            print(f"Target duration is {total_duration:.2f} seconds.")

            print("Processing video clips...")
            clips = []
            current_duration = 0

            # Loop through b-roll paths until we fill the audio duration
            # If not enough paths, we cycle through them
            if not b_roll_paths:
                print("No B-roll clips provided!")
                return ""

            path_idx = 0
            while current_duration < total_duration:
                path = b_roll_paths[path_idx % len(b_roll_paths)]
                try:
                    clip = VideoFileClip(path)
                    
                    # Remove audio from original stock footage
                    clip = clip.without_audio()
                    
                    # Resize to match output format
                    clip = self.resize_clip(clip)
                    
                    # Check how much of the clip we need
                    remaining = total_duration - current_duration
                    if clip.duration > remaining:
                        clip = clip.subclipped(0, remaining)
                        
                    clips.append(clip)
                    current_duration += clip.duration
                    
                except Exception as e:
                    print(f"Warning: Issue with clip {path} - {str(e)}")
                    
                path_idx += 1

            if not clips:
                print("Error: No valid clips were loaded.")
                return ""

            print(f"Concatenating {len(clips)} clips...")
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Add voiceover audio
            final_video = final_video.with_audio(audio)

            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print("Rendering final video. This may take a while...")
            final_video.write_videofile(
                output_path,
                fps=30,
                codec="libx264",
                audio_codec="aac",
                preset="medium",
                threads=4
            )

            # Cleanup
            for clip in clips:
                clip.close()
            final_video.close()
            audio.close()

            print("Rendering complete!")
            return output_path

        except Exception as e:
            print(f"Error creating video: {str(e)}")
            return ""

if __name__ == "__main__":
    # Test stub
    print("VideoEditor module loaded.")
