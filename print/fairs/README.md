# Career-fair print kit (HQ, Nov 19)

Philip asked for a career-fair strategy on Nov 19 and answered HQ's plan with "fairs go". He'll give talks and sit at a few free tables in Austin from January. HQ asked for this kit by Fri Dec 4.

**Status: DRAFT. HQ shows Philip the words before anything prints.** Nothing here is approved yet.

## What's in a set

`build.py <slug>` writes one folder per event, `print/fairs/<slug>/`:

| File | What it is | How it prints |
| --- | --- | --- |
| `handout.pdf` / `.png` | One-page handout, US Letter, portrait | Office printer, 100% (actual size), any paper. White page; nothing sits within 0.5 in of the edge, so no bleed is needed. |
| `qr-card.pdf` / `.png` | QR card, 3.5 x 2 in, page 1 front, page 2 back | Print shop. Each PDF page is 3.75 x 2.25 in: the 3.5 x 2 in trim plus 0.125 in bleed on every side, no crop marks. Words, the code and Tick stay 0.125 in inside the trim. The PNG shows both sides cut to the trim. |
| `table-sign.pdf` / `.png` | Table sign, US Letter, portrait, read from 6 ft | Office printer, 100%, on card stock if there is some; it fits a standard 8.5 x 11 in acrylic sign holder. Same 0.5 in margin as the handout. |

The first set is `austin-test/`.

## Making a set for an event

```
pip install segno zxing-cpp pillow     # once; Playwright and pdftoppm are already in the session
python3 print/fairs/build.py <slug>    # e.g. austin-test; lowercase letters, digits and hyphens
```

Every QR code opens `https://getday60.com/try?utm_source=career_fair&utm_medium=qr&utm_campaign=<slug>`, and `getday60.com` is printed under each code for people who won't scan.

The script writes nothing unless every check passes:
- **QR codes:** it renders each finished PDF page back to pixels at 300 and 150 dpi, decodes every QR code it finds and fails unless each piece has its code where expected (handout 1, card back 1, card front 0, sign 1) and each decodes to the exact link.
- **Lime:** no text is lime, and each piece has exactly one lime element: its "Try it free on one job" button. Tick's own colors don't count.
- **Margins:** every word, card, the code and Tick sit inside the print margin (0.5 in on Letter, 0.125 in inside the card's trim). Only the sparkles may go nearer the edge.

## The words (HQ, Nov 19)

- Headline: "You met the recruiter. Now reach the people closest to the hire."
- What Day60 does, the site's own line (handout only): "Day60 helps you identify the four people closest to the hire: the hiring manager, their boss, an internal champion and the recruiter." The handout's four cards are those four roles; the recruiter's card is checked, because they met that one.
- The step: "Paste a job link. See the 4 people."
- The action: "Try it free on one job"
- Nothing else that promises anything: no result numbers, no prices, no "free forever", no "verified work emails" (print can't change when a setting does).
- "Phil", never "Philip". Founder facts only from founder.ts; the handout carries none, and none of the three pieces uses any.

## Design

The brand pack (`design-system/`): Bricolage Grotesque ExtraBold for display, DM Sans for body, ink outlines, hard offset shadows, Tick static (waving in the logo, pointing at the code, running on the card front), pink and mint sparkles. Ink on white or cream so it prints cleanly on an office printer; the card front is cream to its bleed. Lime is a fill only, never text, and one lime element per piece.

**Read from 6 ft (the sign).** At 6 ft, 20/20 eyes can just make out capitals about 2.7 mm tall. On the sign, every line of the message has capitals at least three times that, and the main line is bigger than the 5/8 in that the ADA sign standard (703.5.5) sets for reading at 6 ft. Capital heights come from the fonts' own metrics:

| Line | Size | Capital height |
| --- | --- | --- |
| "Now reach the people closest to the hire." | Bricolage 72 pt | 0.66 in (16.8 mm) |
| "You met the recruiter." | Bricolage 46.5 pt | 0.43 in (10.8 mm) |
| "Paste a job link. See the 4 people." | Bricolage 39 pt | 0.36 in (9.1 mm) |
| "Try it free on one job" and "getday60.com" | DM Sans Bold 34.5 pt | 0.34 in (8.5 mm) |

The code on the sign is 2.7 in square, the handout's 1.9 in and the card's 1.2 in, each with a white quiet zone of 4 modules.

## Later (HQ, Nov 19)

With the January batches, and inside the normal cadence: one Instagram and Facebook carousel on what to do the night after a career fair. No extra posts.
