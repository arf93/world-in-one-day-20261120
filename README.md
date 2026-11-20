[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/arf93/world-in-one-day-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/arf93/world-in-one-day-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World in One Day — Friday, 20 November 2026

Entry for make.fun `news-image-20261120`: one image that sums up the
world's news of Friday 20 November 2026. A clean newspaper front page
with six verified stories, each with a hand-drawn pictogram, a bold
headline and one factual summary line.

## The six stories

1. **UKRAINE — "KYIV HIT BY MISSILE DEBRIS"**
   Fire breaks out in a three-storey building in the Obolonskyi
   district; the mayor says crews are on the scene after
   early-morning blasts.

2. **CHINA — "CHINA HOLDS RATES FOR 18TH MONTH"**
   The central bank keeps its loan prime rates at 3.0% and 3.5%; the
   benchmark now matters less as the overnight rate takes over.

3. **JAPAN — "JAPAN INFLATION BEATS 2% TARGET"**
   Core prices rise 2.2% in October, the second month above the Bank
   of Japan's target, cementing a December rate-hike bet.

4. **CLIMATE — "COP31 FACES FINAL DAY WITHOUT A DEAL"**
   The summit enters its closing day in Antalya with no agreement yet;
   a slimmed-down draft drops every mention of fossil fuels.

5. **BRUSSELS — "UK AND EU MEET IN BRUSSELS"**
   The second EU-UK summit opens with Burnham, Costa and von der
   Leyen; food, carbon and youth deals on the table.

6. **GAMING — "GTA VI SALES TOP $2.3 BILLION"**
   Estimates published Friday put first-day sales at $2.36 billion
   and 24.6 million copies, a record for the industry.

## Sources

Reuters · Business Today · UN News · European Council

## Files

- `render.py` — draws the whole page with Python 3 + PIL and writes
  `entry.png` (1024×1024, ≤ 1 MiB).
- `main.ts` — Node 22 entrypoint (standard library only). Copies
  `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`), after
  validating the PNG magic bytes and confirming the copy is byte-identical.
- `entry.png` — the rendered front page.
- `LICENSE` — MIT.

## Run

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
