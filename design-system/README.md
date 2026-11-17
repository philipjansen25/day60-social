# Day60 design system for social (Nov 5)

Built from the public site, getday60.com, so it needs no access to the app repo.

- `fonts/`: Bricolage Grotesque and DM Sans woff2 files from getday60.com/fonts, with their SIL OFL license files.
- `tick/`: the six Tick poses (running, celebrating, waiting, waving, pointing, thinking), taken from the site's prerendered pages as standalone SVGs. **Tick stays static, and never draw other characters.**
- `grounds.py`: cover grounds across the palette (Philip, Nov 13): AA text per ground, cream keylines on ink, white halo on lime, and background shapes (60-mark dial, track lanes, finish tape, confetti). `INK_KEYLINES` gives any inner slide or Reel scene on ink the same cream keylines (HQ, Nov 13).
- `ds.py`: the tokens as Python constants, plus CSS helpers: `page`, `tick(pose, w)`, `.step` numbered blocks, `.bubble` speech bubbles, `.sticker`, `.btn`, `.fill`, `check`, `foot`.

Rules: no lime text on cream or white (use lime as a fill there, with ink text). Lime is never text, on any ground, ink included (HQ, Nov 13). Covers use the grounds in `grounds.py`. Coral text uses #C83F19; #FF5C4D is a ground (ink text only) or decoration, never text. Stickers always carry words. Use invented data only, and label it as an example. Show only what's live on getday60.com.

Feed safe area (Philip via HQ, Nov 16): Instagram may show a 1080x1350 post as its middle 1080x1080. `page()` puts every 1080x1350 body in a content layer; `templates/render_many.js` calls `d60Safe.fit()`, which shrinks that layer around the center just enough that every text, sticker, button, Tick, wordmark and slide marker sits inside y 150 to 1200, then `d60Safe.measure()`, and fails the render if anything still crosses. Background art opts out with a class: `d60-bleed-art` (dial, lanes, tape, confetti) stays full-bleed behind the content; `d60-deco` (sparkles) scales with it but isn't measured. Give any new background shape one of those classes, or it counts as content. Passing PNGs are recorded with their SHA-256 in `safe-area.json`, which `scripts/check-library.mjs` reads; its `waived` map holds files rendered before the rule, each with its measured extent and a reason. Reels (1080x1920) keep their own rule. `D60_SAFE_REPORT=1` measures without writing; `D60_OUT_SUFFIX=_safe` writes new files beside the old.

Example: `2026-11/wk46/build_how_reel.py`.
