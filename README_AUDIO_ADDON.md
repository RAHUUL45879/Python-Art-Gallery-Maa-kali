# Maa Kali — Music add-on (review edition)

Save `add_music.py` directly in the root of `Python_Art_Gallery_Maa_Kali`, beside `render_radiant_31s.py`. Do **not** replace the main renderer or `run.sh`.

The script uses `imageio_ffmpeg`, which is already part of your environment. It automatically finds your existing single MP3 under `audio/` and uses the approved 31-second MP4 in `output/`. The original MP4 and MP3 are **never changed**. The review file is written to `output/` and is ignored by Git.

In VS Code's UCRT64 Git Bash terminal, inside the project folder:

```bash
python add_music.py
explorer.exe "$(cygpath -w output/Maa_Kali_31s_Audio_Review.mp4)"
```

By default, the script uses the **first 31 seconds of the song**, with 1.5-second fade-in, 2-second fade-out, and 72% volume. To try the 31-second section beginning 40 seconds into the song:

```bash
python add_music.py --start 40
```

Do not push the original copyrighted song or the review MP4 to GitHub unless you have the required permissions. The default `.gitignore` excludes `audio/` music and `output/` renders. `add_music.py` is source code and can be committed separately after review.
