"""Add a locally stored soundtrack to the 31-second Maa Kali animation.

The original rendered video is not modified. Audio files stay under audio/
(which is Git-ignored). This script requires only Python 3.11+ and
imageio-ffmpeg already listed in requirements.txt.

Examples (from the project root):
    python add_music.py
    python add_music.py --start 40 --volume 0.6

The --start value is the number of seconds into your song to begin using.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
DURATION = 31.0
AUDIO_EXTS = {'.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg'}


def choose_audio(folder: Path) -> Path:
    tracks = sorted(p for p in folder.iterdir()
                    if p.is_file() and p.suffix.lower() in AUDIO_EXTS)
    if not tracks:
        raise FileNotFoundError(
            f'No music found in {folder}. Put your MP3 in the audio folder.')
    if len(tracks) != 1:
        raise ValueError(
            'More than one music file found. Use --audio to choose one:\n' +
            '\n'.join(f'  {p.name}' for p in tracks))
    return tracks[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', type=float, default=0.0,
                        help='Where to start within the music file, in seconds (default: 0)')
    parser.add_argument('--volume', type=float, default=0.72,
                        help='Music volume multiplier, 0.0 to 1.0 (default: 0.72)')
    parser.add_argument('--fade-in', type=float, default=1.5,
                        help='Fade in duration, in seconds (default: 1.5)')
    parser.add_argument('--fade-out', type=float, default=2.0,
                        help='Fade out duration, in seconds (default: 2.0)')
    parser.add_argument('--audio', type=Path,
                        help='Override the music file (default: auto-detect in audio/)')
    parser.add_argument('--video', type=Path,
                        help='Override the silent input video')
    parser.add_argument('--output', type=Path,
                        help='Override the resulting preview MP4')
    args = parser.parse_args()

    if args.start < 0:
        parser.error('--start cannot be negative')
    if not 0 <= args.volume <= 1:
        parser.error('--volume must be between 0 and 1')
    if not 0 <= args.fade_in <= DURATION or not 0 <= args.fade_out <= DURATION:
        parser.error('Fades must be between 0 and 31 seconds')

    video = args.video or (ROOT / 'output' / 'Maa_Kali_Radiant_31s_Python.mp4')
    if not video.is_file():
        video = ROOT / 'exports' / 'Maa_Kali_Radiant_31s_Python.mp4' if args.video is None else video
    if not video.is_file():
        raise FileNotFoundError(f'Video not found: {video}. First run: bash run.sh full')

    if args.audio is not None:
        audio = args.audio
    else:
        folder = ROOT / 'audio'
        if not folder.is_dir():
            raise FileNotFoundError(f'Audio folder missing: {folder}')
        audio = choose_audio(folder)
    if not audio.is_file():
        raise FileNotFoundError(f'Music file missing: {audio}')

    output = args.output or ROOT / 'output' / 'Maa_Kali_31s_Audio_Review.mp4'
    if output.resolve() == video.resolve() or output.resolve() == audio.resolve():
        parser.error('Output must be different from the original video/audio!')
    output.parent.mkdir(parents=True, exist_ok=True)

    # Pad a short clip if necessary; never stretch or pitch-shift the music.
    # AAC produces broadly compatible audio while the approved video is copied.
    filters = [
        '[1:a:0]aresample=async=1:first_pts=0',
        f'atrim=duration={DURATION}',
        'asetpts=PTS-STARTPTS',
        f'apad=whole_dur={DURATION}',
        f'atrim=duration={DURATION}',
        f'volume={args.volume:.4f}',
    ]
    if args.fade_in:
        filters.append(f'afade=t=in:st=0:d={args.fade_in:.4f}')
    if args.fade_out:
        filters.append(f'afade=t=out:st={DURATION-args.fade_out:.4f}:d={args.fade_out:.4f}')
    audio_filter = ','.join(filters) + '[music]'
    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(video),
        '-ss', str(args.start), '-i', str(audio),
        '-filter_complex', audio_filter,
        '-map', '0:v:0', '-map', '[music]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-t', str(DURATION), '-movflags', '+faststart', str(output),
    ]
    print(f'Video: {video}', flush=True)
    print(f'Music: {audio.name}', flush=True)
    print(f'Song section: {args.start:.1f}–{args.start + DURATION:.1f} seconds', flush=True)
    print(f'Output: {output}', flush=True)
    subprocess.run(cmd, check=True)
    print(f'PASS: Music added, preserving original video: {output}', flush=True)
    print('Duration target: 31 seconds | Video copied | Audio: AAC', flush=True)


if __name__ == '__main__':
    main()
