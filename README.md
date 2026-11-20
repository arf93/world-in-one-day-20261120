[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/arf93/world-in-one-day-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/arf93/world-in-one-day-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# One Day in the World — 20 November 2026

This repository is my entry for make.fun's `news-image-20261120`
bounty: a single picture that tells the story of Friday, 20 November
2026. It is laid out like the front page of a newspaper — a masthead
with the date, then six panels, one per story, each with a small
hand-drawn pictogram, a headline and a one-paragraph summary.

## What happened that day

- **Kyiv hit by missile debris (Ukraine).** A fire breaks out in a
  three-storey building in the Obolonskyi district; the mayor says
  emergency crews are on the scene after early-morning blasts.
- **China holds its rates (China).** The central bank leaves the loan
  prime rates at 3.0% and 3.5% for an eighteenth straight month, as
  the benchmark gives way to the overnight rate.
- **Japan's inflation beats the target (Japan).** Core prices rise
  2.2% in October — the second month above the Bank of Japan's 2%
  target — and a December rate rise looks all but certain.
- **COP31 faces its final day without a deal (Climate).** The summit
  enters its closing day in Antalya with no agreement yet, and the
  slimmed-down draft drops every mention of fossil fuels.
- **The UK and the EU meet (Brussels).** The second EU-UK summit
  opens in Brussels with Burnham, Costa and von der Leyen; food,
  carbon and youth deals are on the table.
- **GTA VI sales top $2.3 billion (Gaming).** Figures published on
  Friday put first-day sales at $2.36 billion and 24.6 million
  copies — a record for the industry.

Reporting behind these stories: Reuters, Business Today, UN News and
the European Council.

## How the entry is built

| File | Purpose |
| --- | --- |
| `render.py` | Draws the front page with Python 3 and Pillow, then writes `entry.png` at 1024×1024 and under 1 MiB. |
| `main.ts` | The Node 22 entry point (standard library only). It checks that `entry.png` is a real PNG and copies its bytes unchanged to the output folder. |
| `entry.png` | The finished front page. |
| `LICENSE` | MIT licence. |

## Reproduce it

```sh
python3 render.py
mkdir -p out
MAKEFUN_OUTPUT_DIR=out node main.ts
```

Running the entry twice writes the same bytes both times.
