import re
from youtube_transcript_api._errors import NoTranscriptFound

def extract_video_id(url):
    regex = r"(?<=v=)[^&#]+"
    match = re.search(regex, url)
    return match.group(0) if match else None

def create_metadata(transcript, start_time=None, end_time=None):
    metadata = {
        'video_id': transcript.video_id,
        'language': transcript.language,
        'language_code': transcript.language_code,
        'video_url': f"https://www.youtube.com/watch?v={transcript.video_id}",
        'start': start_time,
        'end': end_time
    }
    return metadata
