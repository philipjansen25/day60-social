"""Reels with our cover as the first second (HQ, Nov 22).

Buffer can't upload a separate Reel cover: it picks a frame of the video (thumbnailOffset, in ms).
So each Reel gets a new file: 1 s of the cover still (the _grid cover, key content inside the
center 1080x1440), then the v2 video unchanged. In Buffer, thumbnailOffset 500 picks the cover.
The v2 videos stay in the repo. Run from the repo root: python3 2026-11/wk48/build_cover_first.py
"""
import os, subprocess

REELS = [
    ("2027-01/wk04/p03_resume_cover_cobalt_grid.png", "2026-11/wk48/p03_resume_reel_v2.mp4", "2026-11/wk48/p03_resume_reel_v3_cover.mp4"),
    ("2027-01/wk03/p04_one_link_cover_mint_grid.png", "2026-11/wk48/p04_one_link_reel_v2.mp4", "2026-11/wk48/p04_one_link_reel_v3_cover.mp4"),
    # Facebook cut of the One Link Reel (HQ, Nov 23): end sticker "getday60.com".
    ("2027-01/wk03/p04_one_link_cover_mint_grid.png", "2026-11/wk48/p04_one_link_reel_fb.mp4", "2026-11/wk48/p04_one_link_reel_fb_cover.mp4"),
]
for cover, video, out in REELS:
    if os.path.exists(out):  # never re-encode a file library.json already uses
        continue
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-loop", "1", "-framerate", "30", "-t", "1", "-i", cover,
        "-f", "lavfi", "-t", "1", "-i", "anullsrc=r=44100:cl=stereo",
        "-i", video,
        "-filter_complex", "[0:v]scale=1080:1920,format=yuv420p,setsar=1[c];[2:v]setsar=1[v];[c][1:a][v][2:a]concat=n=2:v=1:a=1[ov][oa]",
        "-map", "[ov]", "-map", "[oa]",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", "-map_metadata", "-1", out,
    ], check=True)
    print(out)
