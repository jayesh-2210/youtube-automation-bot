import os
import requests
from dotenv import load_dotenv

load_dotenv()

class VisualsGenerator:
    def __init__(self):
        self.api_key = os.getenv("PEXELS_API_KEY")
        if not self.api_key or self.api_key == "your_pexels_api_key_here":
            print("WARNING: PEXELS_API_KEY is not set. Visuals generation will fail.")
        
        self.headers = {"Authorization": self.api_key}

    def search_videos(self, query: str, per_page: int = 5, orientation: str = "landscape") -> list:
        """
        Searches Pexels for videos related to a keyword query.
        orientation: 'landscape' for standard videos, 'portrait' for Shorts (9:16).
        """
        if not self.api_key:
            return []

        url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}&orientation={orientation}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("videos", [])
        except Exception as e:
            print(f"Error searching Pexels for '{query}': {str(e)}")
            return []

    def download_video(self, video_url: str, output_path: str) -> bool:
        """
        Downloads a video file from a given URL to the output path.
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return False

    def generate_b_roll_for_query(self, query: str, output_dir: str = "assets/video", count: int = 3) -> list:
        """
        Finds and downloads `count` relevant videos for a query.
        Returns a list of local file paths.
        """
        print(f"Searching for landscape visuals matching: '{query}'...")
        videos = self.search_videos(query, per_page=count * 2, orientation="landscape")
        return self._process_videos(videos, query, output_dir, count)

    def generate_shorts_b_roll(self, query: str, output_dir: str = "assets/video", count: int = 3) -> list:
        """
        Finds and downloads `count` portrait (9:16) videos for Shorts.
        """
        print(f"Searching for portrait visuals matching: '{query}'...")
        videos = self.search_videos(query, per_page=count * 2, orientation="portrait")
        return self._process_videos(videos, query, output_dir, count)
        
    def _process_videos(self, videos: list, query: str, output_dir: str, count: int) -> list:
        """Helper to download the best HD files from Pexels results."""
        downloaded_paths = []
        for i, video in enumerate(videos):
            if len(downloaded_paths) >= count:
                break
                
            # Filter for HD links
            video_files = video.get("video_files", [])
            # For portrait, height is the larger dimension, but we just want high quality
            hd_files = [f for f in video_files if f.get("quality") == "hd" or max(f.get("width", 0), f.get("height", 0)) >= 1280]
            
            if not hd_files:
                continue
                
            # Sort by highest resolution (multiplying width * height)
            best_file = sorted(hd_files, key=lambda x: x.get("width", 0) * x.get("height", 0), reverse=True)[0]
            download_link = best_file.get("link")
            
            filename = f"broll_{query.replace(' ', '_')}_{i}.mp4"
            output_path = os.path.join(output_dir, filename)
            
            if self.download_video(download_link, output_path):
                downloaded_paths.append(output_path)
                
        return downloaded_paths

if __name__ == "__main__":
    generator = VisualsGenerator()
    query = "money"
    paths = generator.generate_shorts_b_roll(query, count=2)
    print(f"Downloaded files: {paths}")
