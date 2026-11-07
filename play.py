"""Render the Maa Kali animation and open it in your default video player.

Works on Windows, macOS and Linux. No personal paths or shell setup required.
Run: python play.py  (or: python play.py --preview)
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "audio"
OUTPUT_DIR = ROOT / "output"
SILENT_VIDEO = OUTPUT_DIR / "Maa_Kali_Radiant_31s_Python.mp4"
MUSIC_VIDEO = OUTPUT_DIR / "Maa_Kali_31s_Audio_Review.mp4"
PREVIEW_VIDEO = OUTPUT_DIR / "Radiant_Reveal_4s_Preview.mp4"
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}


def select_music() -> Path | None:
    """Return the sole local track; absence means silent playback."""
    if not AUDIO_DIR.is_dir():
        return None
    music = sorted(p for p in AUDIO_DIR.iterdir()
                   if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS)
    if len(music) > 1:
        raise ValueError(
            "Found multiple audio files in audio/. Leave one track there "
            "to use automatic music mixing, or run with --silent."
        )
    return music[0] if music else None


def open_video(path: Path) -> bool:
    """Ask the desktop OS to play an existing MP4; do not modify it."""
    try:
        if os.name == "nt":
            os.startfile(str(path))  # Available only on Windows.
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=True)
        else:
            if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
                print("No desktop display found; open the file manually.")
                return False
            opener = shutil.which("xdg-open")
            if not opener:
                print("No system video opener found; open the file manually.")
                return False
            subprocess.run([opener, str(path)], check=True, timeout=15)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"Could not open a video player automatically: {exc}")
        return False
    return True


def play(preview: bool = False, silent: bool = False, no_open: bool = False) -> int:
    """Render, optionally add local audio, then open the resulting file."""
    music = None
    if not preview and not silent:
        try:
            music = select_music()
        except ValueError as exc:
            print(f"Audio setup: {exc}", file=sys.stderr)
            return 2

    render_command = [sys.executable, str(ROOT / "render_radiant_31s.py")]
    if preview:
        render_command.append("--preview")
    print("Rendering 4-second preview..." if preview else "Rendering 31-second animation...", flush=True)
    try:
        subprocess.run(render_command, cwd=ROOT, check=True)
        result = PREVIEW_VIDEO if preview else SILENT_VIDEO
        if music is not None:
            print(f"Adding local soundtrack: {music.name}", flush=True)
            subprocess.run([sys.executable, str(ROOT / "add_music.py")],
                           cwd=ROOT, check=True)
            result = MUSIC_VIDEO
        elif not preview:
            print("No soundtrack selected; playing the silent animation.")
    except subprocess.CalledProcessError as exc:
        print(f"Animation failed (exit code {exc.returncode}).", file=sys.stderr)
        return exc.returncode or 1

    if not result.is_file():
        print(f"Expected video not found: {result}", file=sys.stderr)
        return 1
    print(f"\nVideo ready: {result}", flush=True)
    if not no_open:
        open_video(result)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true",
                        help="Render and play a short silent 4-second preview")
    parser.add_argument("--silent", action="store_true",
                        help="Skip automatic background music mixing")
    parser.add_argument("--no-open", action="store_true",
                        help="Create the video without opening a player (CI/headless use)")
    args = parser.parse_args()
    return play(preview=args.preview, silent=args.silent, no_open=args.no_open)


if __name__ == "__main__":
    sys.exit(main())
