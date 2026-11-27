# Career-fair print kit (HQ, Nov 19; words and campaign updated Nov 27)

Philip asked for a career-fair strategy on Nov 19 and answered HQ's plan with "fairs go". He'll give talks and sit at a few free tables in Austin from January. HQ asked on Nov 27 for a handout and a table card for Philip's review on Fri Dec 11.

**Status: DRAFT. Nothing prints before Philip's yes.** HQ shows him the words and the sample set first.

## What's in a set

`build.py <slug>` writes one folder per event, `print/fairs/fair-<slug>/`. Each event gets its own slug, so HQ can count scans per fair:

| File | What it is | How it prints |
| --- | --- | --- |
| `handout.pdf` / `.png` | One-page handout, US Letter, portrait | Office printer, 100% (actual size), any paper. White page; nothing sits within 0.5 in of the edge, so no bleed is needed. |
| `table-card.pdf` / `.png` | Table card, US Letter, portrait, read from 6 ft | Office printer, 100%, on card stock if there is some; it fits a standard 8.5 x 11 in acrylic sign holder. Same 0.5 in margin as the handout. |
| `qr-card.pdf` / `.png` | Pocket QR card, 3.5 x 2 in, page 1 front, page 2 back (optional) | Print shop. Each PDF page is 3.75 x 2.25 in: the 3.5 x 2 in trim plus 0.125 in bleed on every side, no crop marks. Words, the code and Tick stay 0.125 in inside the trim. The PNG shows both sides cut to the trim. |

The sample set is `fair-example/` (slug `example`). The Nov 19 draft set (`austin-test/`) is gone: it used the old words and the old campaign name, and nothing was ever printed from it.

## Making a set for an event

```
pip install segno zxing-cpp pillow     # once; Playwright and pdftoppm are already in the session
python3 print/fairs/build.py <slug>    # e.g. ut-austin-jan; lowercase letters, digits and hyphens
```

Every QR code opens `https://getday60.com/try?utm_source=career_fair&utm_medium=qr&utm_campaign=fair-<slug>`, and `getday60.com` is printed under each code for people who won't scan.

The script writes nothing unless every check passes:
- **QR codes:** it renders each finished PDF page back to pixels at 300 and 150 dpi, decodes every QR code it finds and fails unless each piece has its code where expected (handout 1, table card 1, card front 0, card back 1) and each decodes to the exact link.
- **Lime:** no text is lime, and each piece has exactly one lime element: its "Show me the 4 people" button. Tick's own colors don't count.
- **Margins:** every word, card, the code and Tick sit inside the print margin (0.5 in on Letter, 0.125 in inside the card's trim). Only the sparkles may go nearer the edge.

## The words (HQ, Nov 27)

Only from two live pages, read Nov 27:
- the guide "What to do after a career fair", https://getday60.com/guides/what-to-do-after-a-career-fair
- the homepage, https://getday60.com/

Quoted verbatim:
- "What to do after a career fair" (guide title; handout top line)
- "Skip the pile. Message the person who decides." (homepage headline; handout, table card, card front)
- "Stop applying. Start prospecting." (homepage; table card)
- "Apply the same day, write to the recruiter you met while they still remember you, then write to the hiring manager." (the guide's subhead, first sentence; handout)
- The four step headings on the handout, from the guide: "The same day: write it down and apply", "Write to the recruiter you met", "Find the hiring manager for that role", "If nobody answers"
- "Paste a job link. Day60 finds the four people closest to the hire and writes your first message." (homepage subhead; handout. The card back uses its first part, "Paste a job link. Day60 finds the four people closest to the hire.")
- "Show me the 4 people" (the homepage and guide button; the lime button on every piece)
- "Day60 is free. No card needed." (homepage offer; every piece)

Paraphrased from the guide (the line under each step on the handout):
1. "Apply to the posting the same day."
2. "Within a day: where you met, the exact role and one easy question."
3. "The four people closest to the hire: the hiring manager, their boss, an internal champion and the recruiter."
4. "Try the second channel after two days. One follow-up after seven days. Then stop."

Nothing else: no result numbers, no prices, no capacity numbers, no "verified work emails", no founder facts and no name. If either page changes before printing, rebuild from the new words.

## Design

The brand pack (`design-system/`): Bricolage Grotesque ExtraBold for display, DM Sans for body, ink outlines, hard offset shadows, Tick static (waving in the logo, pointing at the code, running on the card front), pink and mint sparkles. Ink on white or cream so it prints cleanly on an office printer; the card front is cream to its bleed. Lime is a fill only, never text, and one lime element per piece (the "Show me the 4 people" button).

**Read from 6 ft (the table card).** At 6 ft, 20/20 eyes can just make out capitals about 2.7 mm tall. On the table card, the message lines have capitals about three times that or more, and the headline is bigger than the 5/8 in that the ADA sign standard (703.5.5) sets for reading at 6 ft. The small "Day60 is free. No card needed." line is about twice that: readable at the table, not across the room. Capital heights use the same font ratios as the Nov 19 sign (Bricolage about 0.0092 in per pt, DM Sans Bold about 0.0099 in per pt):

| Line | Size | Capital height |
| --- | --- | --- |
| "Skip the pile. Message the person who decides." | Bricolage 76.5 pt | 0.70 in (17.8 mm) |
| "Stop applying. Start prospecting." | Bricolage 33 pt | 0.30 in (7.7 mm) |
| "Show me the 4 people" and "getday60.com" | DM Sans Bold 33 to 34.5 pt | 0.33 to 0.34 in (8.3 to 8.6 mm) |
| "Day60 is free. No card needed." | DM Sans Bold 22.5 pt | 0.22 in (5.6 mm) |

The code on the table card is 2.6 in square, the handout's 1.7 in and the card's 1.2 in, each with a white quiet zone of 4 modules.

## Later (HQ, Nov 19)

With the January batches, and inside the normal cadence: one Instagram and Facebook carousel on what to do the night after a career fair. No extra posts.
