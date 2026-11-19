[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/0xvand/news-19nov/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/0xvand/news-19nov/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The Daily Sum — Thursday 19 November 2026

An entry for make.fun's **news-image-20261119** bounty: sum up the world
news of Thursday 19 November 2026 in one image.

`entry.png` is a one-page broadsheet for the day. The lead is the first-ever
three-way summit of the US, Chinese and Russian presidents in Shenzhen;
around it: the ICJ's genocide ruling against Myanmar, Ukraine's third strike
on the Crimean Bridge in a week, missile exchanges over the Gulf,
Anthropic's record $81bn IPO, COP31's final push in Antalya, and the
Democrats taking both houses of Congress — plus an "also today" strip
(Van Gogh's record sale, the US measles comeback, Bangladesh unrest).

- `main.ts` — the entry program (Node 22, standard library only). It copies
  `entry.png` to `/output/entry.png`, byte for byte, every run.
- `draw.py` — the Pillow script that drew the page from the day's headlines,
  set in real fonts so every word stays crisp at judging size.
- `SOURCES.md` — the reporting behind every headline on the page.

Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Licensed under the MIT License (see `LICENSE`).
