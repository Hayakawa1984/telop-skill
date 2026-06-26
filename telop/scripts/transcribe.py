#!/usr/bin/env python3
"""
Transcribe a video file with Whisper and generate a split SRT file.
Usage: python3 transcribe.py <video_path> <output_srt_path> [max_chars]
"""
import sys
import re
import whisper

def to_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def split_japanese_line(text, max_chars=25):
    if len(text) <= max_chars:
        return [text]
    # Break at natural Japanese points near the midpoint
    break_patterns = ['けど', 'から', 'ので', 'ことで', 'して', 'たり', 'って', 'みたいな', 'ところが', '、', 'が', 'を', 'に', 'で', 'は', 'も']
    mid = len(text) // 2
    best_pos = -1
    best_dist = 999
    for pat in break_patterns:
        for i in range(max(0, mid - 8), min(len(text), mid + 8)):
            if text[i:i+len(pat)] == pat:
                pos = i + len(pat)
                dist = abs(pos - mid)
                if dist < best_dist and 3 < pos < len(text) - 3:
                    best_dist = dist
                    best_pos = pos
        if best_pos > 0:
            break
    if best_pos <= 0:
        best_pos = mid
    return [text[:best_pos].strip(), text[best_pos:].strip()]

def main():
    video_path = sys.argv[1]
    output_path = sys.argv[2]
    max_chars = int(sys.argv[3]) if len(sys.argv) > 3 else 25

    print(f"Loading Whisper medium model...", flush=True)
    model = whisper.load_model("medium")
    print(f"Transcribing {video_path}...", flush=True)
    result = model.transcribe(video_path, language='ja', word_timestamps=True)

    blocks = []
    idx = 1
    for seg in result['segments']:
        start = seg['start']
        end = seg['end']
        text = seg['text'].strip()
        if not text:
            continue
        if len(text) > max_chars:
            parts = split_japanese_line(text, max_chars)
            duration = (end - start) / len(parts)
            for i, part in enumerate(parts):
                s = start + i * duration
                e = start + (i + 1) * duration
                blocks.append(f"{idx}\n{to_srt_time(s)} --> {to_srt_time(e)}\n{part}")
                idx += 1
        else:
            blocks.append(f"{idx}\n{to_srt_time(start)} --> {to_srt_time(end)}\n{text}")
            idx += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(blocks) + '\n')

    print(f"SRT saved: {output_path} ({idx-1} entries)", flush=True)

if __name__ == '__main__':
    main()
