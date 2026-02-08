import os
import requests
import json
from bs4 import BeautifulSoup
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    'gemini-flash-lite-latest',
    generation_config={"response_mime_type": "application/json"}
)

# --- Helpers ---
def is_youtube_url(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

def extract_youtube_video_id(url: str) -> str | None:
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    return None

# --- Scrapers ---
def fetch_youtube_transcript_text(video_id: str, prefer=("ko", "en")) -> str:
    try:
        tl = YouTubeTranscriptApi().list(video_id)
        # 1. Try generated/manual based on preference
        try:
            t = tl.find_generated_transcript(list(prefer))
        except:
             # Fallback to any manual transcript
            t = next((tr for tr in tl if not tr.is_generated), None)
            
        if not t:
            t = next(iter(tl), None) # Fallback to first available

        if t:
            snips = t.fetch()
            # Fetch full transcript for AI summary, not just 80 lines
            return " ".join(s["text"] for s in snips) 
        return ""
    except Exception as e:
        print(f"YouTube Transcript Error: {e}")
        return ""

def scrape_website(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        title = soup.title.string if soup.title else "No Title"
        
        # Try to get main content
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text_content = soup.get_text(separator=" ", strip=True)
        return title, text_content[:20000] # Limit to 20k chars context
        
    except Exception as e:
        print(f"Scraping Error: {e}")
        return "Error", ""

# --- AI Analysis ---
def analyze_content(content_text: str):
    system_prompt = """
    You are an expert content curator for a Korean user. 
    Analyze the provided text (or transcript) and return a JSON object.

    Output Fields:
    1. category (string): Choose EXACTLY one from [Tech, Economy, Humor, Life, Politics, Other].
    2. tags (array of strings): 3-5 relevant keywords (Korean).
    3. summary_front (string): A single, catchy, one-line summary (Korean) for a card preview.
    4. content_back (string): A high-quality, structured summary (Korean). 
       - Length: Approximately a 2-minute read.
       - Style: Professional yet easy to read (Smart Brevity style). 
       - Format: Use bullet points or short paragraphs. Markdown is allowed.

    Ensure valid JSON output.
    """
    
    try:
        response = model.generate_content(
            f"{system_prompt}\n\n[Input Content]:\n{content_text}"
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return {
            "category": "Other", 
            "tags": ["Error"], 
            "summary_front": "분석에 실패했습니다.", 
            "content_back": "콘텐츠를 분석하는 도중 오류가 발생했습니다."
        }

def analyze_image(image_bytes: bytes, content_type: str | None):
    system_prompt = """
    You are an expert content curator for a Korean user.
    Analyze the provided image and return a JSON object.

    Output Fields:
    1. category (string): Choose EXACTLY one from [Tech, Economy, Humor, Life, Politics, Other].
    2. tags (array of strings): 3-5 relevant keywords (Korean).
    3. summary_front (string): A single, catchy, one-line summary (Korean) for a card preview.
    4. content_back (string): A detailed description and insight derived from the image (Korean).
       - Length: Approx 1-2 minute read.
       - Style: Insightful.

    Ensure valid JSON output.
    """
    
    try:
        image_part = {
            "mime_type": content_type or "image/jpeg",
            "data": image_bytes,
        }
        response = model.generate_content([system_prompt, image_part])
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini Image Error: {e}")
        return {
            "category": "Other", 
            "tags": ["Image"], 
            "summary_front": "이미지 분석 실패", 
            "content_back": "이미지를 분석할 수 없습니다."
        }