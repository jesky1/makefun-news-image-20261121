[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/jesky1/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/jesky1/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Day — Saturday 21 November 2026

A single-page newspaper front page, typeset as a 1024×1024 PNG, summing up the world news of Saturday 21 November 2026. The page is composed deterministically with Python and Pillow: a masthead, a lead photograph of air defenses over Kyiv at dawn, a lead story, four secondary stories in two columns, an "Also Today" briefs band, and a source footer. The hero photograph (`hero.webp`) is centre-cropped into the layout and the whole page is rendered by measuring real font metrics, so the result is reproducible from the sources in this repository.

## Stories

- **Lead — Russian Missiles Fall in Poland as Massive Barrage Pounds Ukraine:** Russia fired more than 400 drones and 110 missiles at Ukraine overnight, killing at least eight people in Kyiv, while two missiles and a suspected drone came down in southeastern Poland, which Prime Minister Donald Tusk called a deliberate provocation.
- **NEW YORK — AI Sell-Off Pushes S&P 500 Into Correction:** US stocks fell 3.7% on Friday as a rout in AI and chip shares pushed the S&P 500 and the Dow into correction territory and wiped out the Nasdaq's gains for the year.
- **LONDON — Cancer Pill Erases Tumours in Trial:** A trial of the pill daraxonrasib found pancreatic cancer became undetectable on scans in one in 12 patients, a rare breakthrough against one of the deadliest cancers.
- **BRUSSELS — UK and EU Sign Biggest Post-Brexit Agreements:** Prime Minister Andy Burnham and EU leaders signed three agreements covering food exports, carbon markets and youth mobility, the biggest step in UK-EU relations since Brexit.
- **ANTALYA — COP31 Talks Run Past Deadline in Fossil-Fuel Deadlock:** The UN climate summit in Antalya, Turkey, ran into overtime as nearly 200 nations failed to agree on language over fossil fuels.
- **Also Today:** Briefs cover a reported hack of the FBI criminal database, Iran saying it downed a US MQ-9 drone over the Strait of Hormuz, a US judge validating Bayer's $7.25 billion Roundup settlement, a magnitude 6.9 earthquake in the Peruvian Andes, a conviction over Los Angeles' deadly Palisades fire, and swimmer Lewis Pugh crossing the Strait of Hormuz to spotlight the war's toll on wildlife.

Sources: Compiled from news reporting of Saturday 21 November 2026 — wire services and international outlets.

## Run

Rebuild the front page image:

```sh
python3 compose.py
```

Copy the entry image to the output directory (defaults to `/output`):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` uses only the Node standard library. It verifies that `entry.png` is non-empty, at most 1 MiB, and starts with the PNG signature before and after copying.

## License

MIT — see [LICENSE](LICENSE).
