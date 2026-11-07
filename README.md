# Python Art Gallery — Maa Kali

**A 31-second devotional animation built frame by frame with Python.**  
*A Mitratics creative-coding project.*

[Watch the current silent preview](exports/Maa_Kali_Radiant_31s_Python.mp4) · [Explore the renderer](render_radiant_31s.py) · [See the tests](tests/test_radiant_movie.py)

**Film:** 432 × 768 (portrait) · 20 FPS · 620 frames · H.264 MP4  
**Status:** Working development version. Music, the final release, and public licensing are still being prepared.

> **How it is made:** Python draws the opening M, Mahadev, the ending, smoke, sparks, lighting, and transitions. The approved **16-frame Maa Kali GIF** in `assets/` provides the central character reveal. Python blends that artwork into the scene and encodes the complete video. The renderer does **not** use a finished MP4 as input. This is Python-produced animation, **not a fully code-drawn Kali character**.

## How the animation works

```text
Frame number (0–619)
        ↓
render_radiant_31s.py → render_frame(frame_number)
        ↓
Scene 1 / Scene 2 / Scene 3
        ↓
Pillow draws and combines the visual layers → one RGB image
        ↓
imageio-ffmpeg encodes RGB frames → output/*.mp4
```

| Time | Scene | Python work |
|---|---|---|
| **0.0–7.6s** | Golden M | Draw curved paths, glowing rings, smoke and drifting particles in `code_art/scene1.py`. |
| **7.6–25.3s** | Mahadev and Maa Kali | Animate the approved GIF, blend adjacent frames, draw Mahadev in front, and add mist and embers in `render_radiant_31s.py` and `code_art/eyes_shiva.py`. |
| **25.3–31.0s** | Greeting | Draw the M, “Happy Kali Puja”, “Coming Soon”, and background effects in `code_art/scene3.py`. |

**The main idea:** A video is a sequence of images. At 20 FPS, Python creates 20 images for every second. `render_frame(index)` chooses the scene; Pillow creates the image; FFmpeg joins the images into a playable video.

## Libraries and where they are used

Only **two external Python packages** are required by the current video renderer. See [`requirements.txt`](requirements.txt).

| Package | Official link | Used for | Main APIs in this project |
|---|---|---|---|
| **Pillow** (`PIL`) | [Docs](https://pillow.readthedocs.io/en/stable/) · [Source](https://github.com/python-pillow/Pillow) | Draw shapes and text, read GIF frames, blur glow, combine layers | `Image`, `ImageDraw`, `ImageFilter`, `ImageFont`, `Image.blend`, `alpha_composite` |
| **imageio-ffmpeg** | [Docs and source](https://github.com/imageio/imageio-ffmpeg) · [PyPI](https://pypi.org/project/imageio-ffmpeg/) | Encode frames into an H.264 MP4 with FFmpeg | `write_frames()`; `get_ffmpeg_exe()` for future audio work |

**Built into Python (no extra install):** [`math`](https://docs.python.org/3/library/math.html) for curves and movement, [`random`](https://docs.python.org/3/library/random.html) for repeatable particle patterns, [`pathlib`](https://docs.python.org/3/library/pathlib.html) for file paths, [`argparse`](https://docs.python.org/3/library/argparse.html) for render options, [`functools.lru_cache`](https://docs.python.org/3/library/functools.html) to reuse Shiva drawings, and [`unittest`](https://docs.python.org/3/library/unittest.html) for tests.

**Encoding:** `imageio-ffmpeg` provides FFmpeg for the supported installation. The renderer outputs H.264 (`libx264`) with `yuv420p` pixel format for broad playback support. [FFmpeg documentation](https://ffmpeg.org/documentation.html).

## Code map — where should I make changes?

| File | What it does | Change it when you want to… |
|---|---|---|
| [`render_radiant_31s.py`](render_radiant_31s.py) | Main entry point; frame timing, scene selection, GIF interpolation, compositing and MP4 export | Adjust timing, transitions, canvas size, frame rate or output |
| [`code_art/scene1.py`](code_art/scene1.py) | Draws the M with Bézier paths, orbital rings, glow and embers | Improve the opening logo or particles |
| [`code_art/eyes_shiva.py`](code_art/eyes_shiva.py) | Draws dark atmosphere, glowing eyes, smoke and foreground Mahadev | Change the reveal and scene atmosphere |
| [`code_art/shiva_approved.py`](code_art/shiva_approved.py) | Draws Mahadev’s pose, hair and fire/smoke details | Improve the character drawing |
| [`code_art/scene3.py`](code_art/scene3.py) | Draws the ending logo, greeting and “Coming Soon” | Change text, typography or ending effects |
| [`assets/maa_kali_radiant_reveal.gif`](assets/maa_kali_radiant_reveal.gif) | Approved Kali character frames | Update the character animation asset |
| [`tests/test_radiant_movie.py`](tests/test_radiant_movie.py) | Checks timing, frame size, animation changes and scene boundaries | Add automated quality checks |
| [`.github/workflows/python-tests.yml`](.github/workflows/python-tests.yml) | Runs tests on GitHub after pushes and pull requests | Extend continuous integration (CI) |

**Key functions to look for:** `scene1.render_frame()`, `load_reference_frames()`, `asset_position()`, `middle_frame()`, `shiva_layer()`, `scene3.render_frame()`, and `render_video()`.

The core timing values are easy to find:

```python
# render_radiant_31s.py
W, H = 432, 768
FPS = 20
OPENING, MIDDLE, ENDING = 152, 354, 114
FRAMES = OPENING + MIDDLE + ENDING  # 620 frames / 20 FPS = 31 seconds
```

**Visual techniques:** Bézier curves draw smooth paths; a changing frame index creates motion; RGBA layers allow transparency; `GaussianBlur` makes light glow; `Image.blend()` makes smooth transitions. In Scene 2, `CUES` controls when the 16 GIF frames appear across 17.7 seconds, and cached Shiva layers avoid repeated heavy drawing.

## Run the project

Install **Python 3.11+** and the project dependencies (a virtual environment is recommended):

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Render a single frame, a short preview, or the full silent movie:

```bash
python render_radiant_31s.py --still 355
python render_radiant_31s.py --preview
python render_radiant_31s.py
```

The full render is written to `output/Maa_Kali_Radiant_31s_Python.mp4`. Generated files in `output/` are ignored by Git. The `exports/` video is the saved development baseline. On a system with Bash, `bash run.sh test`, `bash run.sh preview`, and `bash run.sh full` are shortcuts. If `python` is unavailable, use your system's Python command or virtual-environment interpreter.

## Audio — the next feature

The current main renderer produces a **silent video**. The `audio/` folder is for local music; audio recordings are excluded from Git. The final soundtrack mix is not yet part of the tracked render pipeline.

Audio can be added after video rendering by calling FFmpeg from Python with [`subprocess`](https://docs.python.org/3/library/subprocess.html). For example, a future `add_music.py` could run:

```python
import subprocess
import imageio_ffmpeg

subprocess.run([
    imageio_ffmpeg.get_ffmpeg_exe(), "-y",
    "-i", "output/Maa_Kali_Radiant_31s_Python.mp4",
    "-stream_loop", "-1", "-i", "audio/background_music.mp3",
    "-filter_complex", "[1:a]atrim=0:31,asetpts=PTS-STARTPTS,"
                       "volume=0.35,afade=t=in:st=0:d=1,"
                       "afade=t=out:st=29:d=2[a]",
    "-map", "0:v:0", "-map", "[a]", "-t", "31",
    "-c:v", "copy", "-c:a", "aac", "output/Maa_Kali_With_Music.mp4",
], check=True)
```

**This is a proposed example, not a command the current renderer runs.** It loops a local track if needed, trims it to 31 seconds, lowers volume, adds fades, and combines the audio with the video. Use music you have permission to publish.

## Contribute and develop

![Creators worldwide are invited: any language, background or skill level. Share code, art, sound, knowledge, feedback and ideas. Every perspective helps us learn, build and grow together.](assets/contribute-banner.svg)

**Make it yours:** Pick a scene or feature from the **Code map** above, improve it, and run `--preview` and the tests. When contributions open, share your work through a pull request. **All ideas are welcome; changes to `main` are reviewed before merging.**

**Quick Git:** `git status` → `git add .` → `git commit -m "Describe change"` → `git push`. [GitHub Actions](.github/workflows/python-tests.yml) checks the tests, but does not yet render the full movie in CI.

**Versions and rights:** Git history records development; completed editions will use GitHub Releases. Public code licensing, artwork permissions, and contribution rules are still being prepared. The video, GIF, Mitratics branding, and third-party music are not automatically covered by a future code license.

---

**Made with Python · A Mitratics project · Built for creative developers.**
