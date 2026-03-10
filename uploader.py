import os
import datetime
from dotenv import load_dotenv

load_dotenv()
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class YouTubeUploader:
    def __init__(self, client_secrets_file="client_secrets.json"):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.client_secrets_file = client_secrets_file
        self.credentials = None

    def _authenticate(self):
        """
        Authenticates the user and returns the constructed YouTube resource.
        Saves credentials to 'token.json' to prevent re-prompting.
        """
        if os.path.exists("token.json"):
            self.credentials = Credentials.from_authorized_user_file("token.json", self.scopes)
        
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                # Parse credentials either from env or from file
                client_id = os.getenv("GOOGLE_CLIENT_ID")
                client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
                
                if client_id and client_secret:
                    client_config = {
                        "installed": {
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                        }
                    }
                    flow = InstalledAppFlow.from_client_config(client_config, self.scopes)
                else:
                    if not os.path.exists(self.client_secrets_file):
                        print(f"ERROR: {self.client_secrets_file} not found. You must either set GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET in .env or download the generic credentials JSON.")
                        return None
                    flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
                
                self.credentials = flow.run_local_server(port=0)
                
            # Save token for next loops
            with open("token.json", "w") as f:
                f.write(self.credentials.to_json())

        return build("youtube", "v3", credentials=self.credentials)

    def upload_video(self, video_path: str, title: str, description: str, tags: list, category_id: str = "22", privacy_status: str = "private") -> str:
        """
        Uploads a video to YouTube.
        """
        youtube = self._authenticate()
        if not youtube:
            print("Authentication failed.")
            return None

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status, # Keep private for the bot testing phase
                "selfDeclaredMadeForKids": False
            }
        }

        # Media handle
        try:
            print(f"Starting upload for '{title}'...")
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            
            request = youtube.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media
            )
            
            # Simple resume upload logic
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Uploaded {int(status.progress() * 100)}%.")

            video_id = response.get('id')
            print(f"Upload complete! Video ID: {video_id}")
            return video_id
            
        except Exception as e:
            print(f"Upload failed: {str(e)}")
            return None

if __name__ == "__main__":
    print("YouTubeUploader module loaded.")
    # Instructions to the user:
    # 1. Create a Google Cloud Project
    # 2. Enable YouTube Data API v3
    # 3. Create OAuth 2.0 Client IDs (Desktop)
    # 4. Download JSON and save as 'client_secrets.json' in the root folder.
