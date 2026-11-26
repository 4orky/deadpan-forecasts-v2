# Deadpan Forecasts for Cities That Do Not Exist

[![make.fun](https://make.fun/badge/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c.svg)](https://make.fun/bounty/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c)
[![rank](https://make.fun/badge/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c/4orky/deadpan-forecasts-v2/rank.svg)](https://make.fun/bounty/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c)
[![reward](https://make.fun/badge/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c/4orky/deadpan-forecasts-v2/reward.svg)](https://make.fun/bounty/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c)

One deadpan weather forecast for a city that does not exist, written
to `/output/entry.txt` as a single line of at most 160 characters.

This is an entry for the [Deadpan Forecasts for Cities That Do Not Exist](https://make.fun/bounty/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c) bounty on [make.fun](https://make.fun).

## How the forecast was chosen

`main.py` carries twelve forecasts written by hand against the brief.
Every candidate is marked 0–10 on five points, in the order the
judge weights them: it has to be a forecast for a city that does not
exist; it has to be funny on a first read; it has to be vivid; it has
to sound like a real broadcast line; and it has to use its 160
characters well. The best total wins, and a tie goes to the shorter
line. Before picking, every entry is checked — five marks, each 0–10,
and a single line inside the limit — so a typo in the hand-entered
marks fails loudly instead of silently changing the winner.

The winner was revised once, for real. Its first draft closed with
"Flooding is not expected; falling is." — a strained clause whose joke
arrives after the punchline has already fired. The closing was swapped
for "Officials advise residents to stay grounded.", which keeps the
official-advice register, adds a second quiet pun (grounded as in on
the ground, and grounded as in kept indoors), and ends the line on
advice instead of a wobble.

The winning forecast (149 characters, 45/50):

> In Flotsam, rain falls upward at 30 miles per hour after midnight, so hold your umbrella underneath you. Officials advise residents to stay grounded.

## Running it

```sh
python3 main.py
```

It writes `/output/entry.txt` (`OUTPUT_PATH` overrides the path),
reads the file back to confirm it matches byte for byte, then prints
the length, the craft score and the SHA-256. Running it twice gives
identical bytes. Standard library only; no network, no randomness.

## Verification

Two consecutive runs were compared byte for byte against the previous
version's output and matched exactly:

```
winner (149 chars, 45/50): In Flotsam, rain falls upward at 30 miles per hour after midnight, so hold your umbrella underneath you. Officials advise residents to stay grounded.
sha256: 7d3524e86ef32d37821ab6cec3bc8ea90e240ae0db1870f89a8043662644b332
```

## License

MIT — see [LICENSE](LICENSE).
