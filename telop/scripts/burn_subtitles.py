#!/usr/bin/env python3
"""
Burn an SRT file into a video using imageio-ffmpeg (which includes libass).
Also trims the video to the last subtitle end time + 0.5s.
Usage: python3 burn_subtitles.py <video_path> <srt_path> <output_path>
"""
import sys
import re
import shutil
import subprocess

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    print("Error: imageio-ffmpeg not installed. Run: pip3 install imageio-ffmpeg", file=sys.stderr)
    sys.exit(1)

STYLE = "FontName=Hiragino Sans,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=30"

def get_last_subtitle_time(srt_path):
    with open(srt_path) as f:
        content = f.read()
    times = re.findall(r'--> (\d{2}:\d{2}:\d{2},\d{3})', content)
    if not times:
        return None
    h, m, s = times[-1].split(':')
    s, ms = s.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def main():
    video_path = sys.argv[1]
    srt_path = sys.argv[2]
    output_path = sys.argv[3]

    # Copy SRT to /tmp to avoid issues with special characters in path
    tmp_srt = '/tmp/telop_subtitles.srt'
    shutil.copy2(srt_path, tmp_srt)

    trim_time = get_last_subtitle_time(srt_path)
    trim_args = ['-t', str(trim_time + 0.5)] if trim_time else []

    cmd = [
        FFMPEG,
        '-i', video_path,
        *trim_args,
        '-vf', f"subtitles={tmp_srt}:force_style='{STYLE}'",
        '-c:a', 'copy',
        '-y', output_path
    ]

    print(f"Burning subtitles (trim to {trim_time + 0.5:.1f}s)...", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-2000:], file=sys.stderr)
        sys.exit(1)
    print(f"Done: {output_path}", flush=True)

if __name__ == '__main__':
    main()
