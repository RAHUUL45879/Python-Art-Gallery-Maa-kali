# Python Art Gallery — Maa Kali

**Approved 31-second Kali Puja film — source, visual asset, tests and final silent MP4.**

- **Opening**: golden M, 7.6 seconds (152 frames)
- **Middle**: Maa Kali reveal and meditating Mahadev, 17.7 seconds (354 frames)
- **Ending**: greeting and Coming Soon, 5.7 seconds (114 frames)
- **Total**: 31.0 seconds, 20 FPS, 432 × 768, 620 frames
- **No lion.**

## How this version was made

Python draws the opening, Mahadev, closing, lights/embers, blends the supplied **approved animated Kali GIF** in the middle, and encodes the final MP4. It does **not** use a completed MP4 as input. The Kali character is not generated exclusively from primitive drawing commands.

## Windows / VS Code / UCRT64 Git Bash

Recommended folder: `C:\Development\Projects\Python_Art_Gallery_Maa_Kali`

The Python 3.11 virtual environment already configured is located at:
`C:\Development\VirtualEnvironments\mitratics-kali-puja-python`

In UCRT64 Git Bash, while inside the project:

```bash
bash run.sh test
bash run.sh preview
bash run.sh full
```

Or use the virtual environment explicitly:

```bash
PY="/c/Development/VirtualEnvironments/mitratics-kali-puja-python/Scripts/python.exe"
"$PY" -m pip install -r requirements.txt
"$PY" -m unittest discover -s tests -v
"$PY" render_radiant_31s.py --preview
"$PY" render_radiant_31s.py
```

The generated video is saved as `output/Maa_Kali_Radiant_31s_Python.mp4`. The approved original video is also in `exports/` (tracked in Git).

See [docs/SETUP_AND_GITHUB.md](docs/SETUP_AND_GITHUB.md) for private GitHub setup.

## Folders

- `code_art/`: drawing and animation modules.
- `assets/`: approved animated Kali visual.
- `audio/`: future background music, **excluded from Git** by default.
- `exports/`: approved final video, included in Git.
- `output/`: locally generated renders, **excluded from Git**.
- `tests/`: automated rendering/timeline checks.
- `.github/workflows/`: GitHub Actions test automation (no costly full render).
- `docs/`: setup and project documentation.

## Notes

- Your original separate `Mitratics_Kali_Puja_Python_Starter` demo is unrelated and should not be copied into this repository.
- Your working old project versions should be backed up *outside* this final folder before replacing them.
- Audio has not yet been added. Keep copyrighted recordings out of GitHub unless you have the appropriate rights.
