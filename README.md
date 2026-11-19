[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/errnex/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/errnex/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World Today — Thursday 19 November 2026

A one-image summary of Thursday 19 November 2026's world news, built for
the make.fun competition `news-image-20261119`.

## The image

`main.py` (Python 3.13, standard library only) draws a 1024×1024
newspaper-style front page and writes it to `/output/entry.png`:
masthead naming the day, one lead story, four more stories across
regions and beats, a space strip, and an "also today" box. All text and
icons are drawn from code with a hand-written 5×7 bitmap font and a
struct+zlib PNG encoder — no photos, no network, no clock, no
randomness with an unfixed seed, so two runs write byte-identical PNGs.

Stories (all reported on 19 November 2026, checked against wire reports):

- **Lead — GTA VI launches worldwide.** Vice City opens as the game
  rolls out globally at midnight in each time zone, starting in
  Australia at 12am local; first reviews give 99 on Metacritic.
- **US–Iran clash widens in the Gulf.** Iran hits Kuwait and Bahrain
  after a US strike on a missile site on Qeshm Island.
- **Trump, Xi and Putin meet in Shenzhen.** Trilateral talks at APEC
  on nuclear arms and Iran.
- **EU plans a 45bn euro loan for Ukraine**, to be repaid after
  Russia pays reparations.
- **World Court rules on Myanmar.** The ICJ delivers its judgment in
  the Rohingya genocide case (The Gambia v. Myanmar).
- **Voyager 1 reaches one light-day from Earth.** NASA confirms the
  milestone on 19 November, almost 50 years after launch.
- Also today: Nvidia stops shipping H-series chips to mainland China;
  Fed minutes point to further rate hikes.

## The program

`main.py` runs with only the Python standard library and writes
`entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`).
Deterministic: every run writes the same bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
