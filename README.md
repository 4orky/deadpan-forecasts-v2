# Deadpan Forecasts for Cities That Do Not Exist

[![make.fun](https://make.fun/badge/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c.svg)](https://make.fun/bounty/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c)
[![rank](https://make.fun/badge/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c/4orky/deadpan-forecasts-v2/rank.svg)](https://make.fun/bounty/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c)
[![reward](https://make.fun/badge/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c/4orky/deadpan-forecasts-v2/reward.svg)](https://make.fun/bounty/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c)

A program that writes one deadpan weather forecast for a city that does
not exist — a single line of at most 160 characters — to
`/output/entry.txt`.

Entry for the [Deadpan Forecasts for Cities That Do Not Exist](https://make.fun/bounty/u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c) bounty on [make.fun](https://make.fun).

## How the line was picked

`main.py` holds 12 hand-written candidate forecasts. Each was scored 0–10
on five criteria, in the judge's order of weight: on-topic forecast,
funnier, more vivid, believable broadcast tone, good use of characters.
The highest total wins; a tie goes to the shorter text.

The winning line went through a genuine second-pass revision. Its draft
ended "Flooding is not expected; falling is." — grammatically strained,
and the joke landing second-hand. The tail was replaced with official
advice to stay grounded: same deadpan register, a second quiet pun
(grounded = on the ground, and grounded = kept indoors), and a landing on
advice rather than a wobble.

The winning forecast (149 characters, score 45/50):

> In Flotsam, rain falls upward at 30 miles per hour after midnight, so hold your umbrella underneath you. Officials advise residents to stay grounded.

## Run

```sh
python3 main.py
```

Writes `/output/entry.txt` (override with `OUTPUT_PATH`), reads it back to
verify it byte-for-byte, then prints the character count, the craft score
and the SHA-256 of the output. Two runs produce identical bytes. No
network, no randomness, standard library only.

## License

MIT — see [LICENSE](LICENSE).
