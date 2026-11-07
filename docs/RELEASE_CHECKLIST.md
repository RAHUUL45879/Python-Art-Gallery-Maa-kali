# v1.0.0 publication checklist (not yet released)

This document is a private maintainer checklist. Do not interpret it as proof that a release has been published.

- [x] 14 local automated tests passed in the user's VS Code session (7 Nov 2026).
- [x] `bash play --preview` locally rendered 80 frames / 4 seconds (7 Nov 2026).
- [x] Commit `8f54a14` pushed to `main` with a clean `git status -sb` (7 Nov 2026).
- [ ] Latest GitHub Actions run for `8f54a14` verified successful.
- [ ] Code/documentation license accepted by the copyright holder; related files committed.
- [ ] Ownership and public distribution rights confirmed for bundled GIF, SVG and silent MP4.
- [ ] Rights to any proposed public music or music-containing MP4 confirmed; otherwise publish no such audio.
- [ ] Decide whether the repo should be public; do not change visibility until the owner approves.
- [ ] Run `python -m unittest discover -s tests -v` and `python play.py --no-open` after the final docs commit.
- [ ] Inspect `git status -sb` and `git diff --cached --name-only` before pushing; exclude local audio and videos.
- [ ] Only after all checks, create annotated tag `v1.0.0` at the intended commit and publish GitHub Release with cleared assets only.

**Suggested release notes (after approval):** 31-second 432×768 Python-rendered Maa Kali animation, cross-platform one-command playback, optional *local* soundtrack integration, 14 automated tests, contribution guidance. State clearly that the main character reveal uses a bundled GIF asset.
