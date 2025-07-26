import os
import subprocess
import re
from typing import List, Optional

LANGUAGE_CODE_REGEX = re.compile(r'\.(?P<lang>[a-z]{2})\.(srt|vtt)$', re.IGNORECASE)

class SubtitleExtractor:
    """
    Extracts embedded subtitles from video files and saves them in the correct format and naming convention.
    """
    def __init__(self, video_path: str, output_dir: Optional[str] = None):
        self.video_path = video_path
        self.output_dir = output_dir or os.path.dirname(video_path)
        self.scene_file_name = os.path.splitext(os.path.basename(video_path))[0]

    def extract_subtitles(self):
        """
        Extracts all embedded subtitles using ffmpeg and saves them as SRT files.
        """
        # Get subtitle streams
        cmd = [
            'ffmpeg', '-i', self.video_path
        ]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        streams = self._parse_streams(result.stderr)
        for stream in streams:
            self._extract_stream(stream)

    def _parse_streams(self, ffmpeg_output: str) -> List[dict]:
        # Parse subtitle streams from ffmpeg output
        streams = []
        for line in ffmpeg_output.splitlines():
            if 'Subtitle:' in line:
                match = re.search(r'Stream #(\d+):(\d+)(\(\w+\))?: Subtitle: ([^,]+)(.*)', line)
                if match:
                    stream_index = match.group(2)
                    lang_match = re.search(r'lang:([a-z]{2})', line)
                    lang = lang_match.group(1) if lang_match else 'unknown'
                    streams.append({'index': stream_index, 'lang': lang})
        return streams

    def _extract_stream(self, stream: dict):
        lang = stream['lang']
        index = stream['index']
        out_name = f"{self.scene_file_name}.{lang}.srt" if lang != 'unknown' else f"{self.scene_file_name}.srt"
        out_path = os.path.join(self.output_dir, out_name)
        cmd = [
            'ffmpeg', '-i', self.video_path, '-map', f'0:s:{index}', out_path, '-y'
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Plugin hooks

def on_scene_scan(video_path: str):
    extractor = SubtitleExtractor(video_path)
    extractor.extract_subtitles()

def retroactive_subtitle_task(video_paths: List[str]):
    for path in video_paths:
        extractor = SubtitleExtractor(path)
        extractor.extract_subtitles()
