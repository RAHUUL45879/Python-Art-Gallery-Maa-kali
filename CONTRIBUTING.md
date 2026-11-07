# Contributing to Python Art Gallery — Maa Kali

Thank you for supporting this Mitratics creative-coding project. Developers, artists, learners and reviewers of all experience levels are welcome. Feedback, accessibility improvements, performance fixes, documentation and animation ideas are useful contributions.

## First steps

1. Read [`README.md`](README.md), [`LICENSE`](LICENSE) and [`ASSET_POLICY.md`](ASSET_POLICY.md).
2. Fork the repository and create a branch for one focused change. Please do not commit directly to `main`.
3. Install dependencies: `python -m pip install -r requirements.txt`.
4. Run tests: `python -m unittest discover -s tests -v`.
5. Render a four-second preview: `python play.py --preview --no-open`.
6. Open a pull request describing what changed, why, and what you tested. Attach before/after screenshots or a short demo **only if you have the rights to share the media**.

## What to contribute

- Python frame drawing, scene improvements, rendering speed and reliability.
- Better developer commands, Windows/macOS/Linux compatibility, tests or CI.
- Documentation, bug fixes, translations, accessibility and beginner-friendly guidance.
- New ideas through an issue before undertaking large rewrites.

## Source-code and asset rules

- Code and documentation contributions are licensed under the repository's **MIT License**.
- Do **not** submit copyrighted songs, recordings, fonts or images without suitable distribution permission. The GIF, video and brand assets in the repository are **not** covered by the MIT code license. See [`ASSET_POLICY.md`](ASSET_POLICY.md).
- Never commit credentials, personal information, local music from `audio/`, or generated files from `output/`.
- Stage selected files explicitly rather than using `git add .` if private media might be present.
- Keep code readable and compatible with the supported Python environment; add or update tests when behavior changes.

## How reviews and credits work

All changes to `main` are approved and merged by the repository maintainer. A successful automated test does not guarantee that a pull request will be accepted. Contributors are credited through GitHub history; optional on-video recognition in future editions requires mutual agreement and must be compatible with distribution rights.

Be constructive and respectful. Explain concerns about code or visual changes clearly, and avoid harassment or abusive conduct.
