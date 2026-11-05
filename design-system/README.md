# Day60 design system for social (Nov 5)

Built from the public site, getday60.com, so it needs no access to the app repo.

- `fonts/`: Bricolage Grotesque and DM Sans woff2 files from getday60.com/fonts, with their SIL OFL license files.
- `tick/`: the six Tick poses (running, celebrating, waiting, waving, pointing, thinking), taken from the site's prerendered pages as standalone SVGs. **Tick stays static, and never draw other characters.**
- `ds.py`: the tokens as Python constants, plus CSS helpers: `page`, `tick(pose, w)`, `.step` numbered blocks, `.bubble` speech bubbles, `.sticker`, `.btn`, `.fill`, `check`, `foot`.

Rules: no lime text on cream or white (use lime as a fill there, with ink text). Lime text or accents on ink/navy are fine. Coral text uses #C83F19, and #FF5C4D is for decoration only. Stickers always carry words. Use invented data only, and label it as an example. Show only what's live on getday60.com.

Example: `2026-11/wk46/build_how_reel.py`.
