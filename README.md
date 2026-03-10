# YouTube Faceless Automation Bot

This project is a fully automated AI video generation pipeline built in Python.

## Features:
1. Picks a trending topic from a selected niche.
2. Writes an engaging storytelling script using **OpenAI (GPT-4o-mini)**.
3. Synthesizes a human-like voiceover using **ElevenLabs**.
4. Discovers and downloads high-quality, relevant B-roll clips via **Pexels API**.
5. Assembles the clips and audio into a final `.mp4` video using **MoviePy**.
6. Uploads the final video to your channel using the **YouTube Data API v3**.

## Setup Instructions

### 1. Install Dependencies
Make sure you are in the virtual environment.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Keys
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Fill out your keys inside `.env` for:
- `OPENAI_API_KEY`
- `ELEVENLABS_API_KEY`
- `PEXELS_API_KEY`

### 3. Setup YouTube Data API Authentication
To enable automatic uploading:
1. Go to the [Google Cloud Console](https://console.cloud.google.com).
2. Create a Project and enable the **YouTube Data API v3**.
3. Go to Credentials, create an **OAuth 2.0 Client ID** (Application type: Desktop App).
4. Download the JSON file and rename it to `client_secrets.json`. Place it in this folder.

### 4. Run the Bot!
```bash
python main.py
```
*Note: The first time you run the script, a browser window will open asking you to log into your Google Account to authorize the YouTube upload. It will save a `token.json` file so it doesn't ask again!*

## Scaling it via Cron
Once tested and working, you can completely automate the script to run daily at a specific time:

```bash
crontab -e
```
Add the following line (run every day at 10 AM):
```
0 10 * * * cd /Users/jayeshg/Desktop/youtube && /Users/jayeshg/Desktop/youtube/venv/bin/python main.py >> automation.log 2>&1
```
