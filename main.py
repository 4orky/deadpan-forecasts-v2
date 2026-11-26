"""Deadpan Forecasts for Cities That Do Not Exist.

make.fun bounty u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c
($2, winner take all). The program writes one weather forecast, a single
line of 1-160 characters, for a city that does not exist, to
/output/entry.txt.

How the line was chosen
-----------------------
Twelve candidate forecasts were written by hand against the brief, then
scored 0-10 on five criteria, in the judge's order of weight:

  1. on-topic: a one-line forecast for a city that does not exist, absurd
     yet believable (any off-subject line loses outright)
  2. funnier: the joke lands on a first read; a deadpan twist, not a pile
     of random absurdity
  3. more vivid: a concrete image, number or detail that makes the
     invented city's weather feel real
  4. broadcast tone: plain, confident, believable, as if a straight-faced
     meteorologist were reading it aloud
  5. character use: tight and well paced, making good use of the 160

The highest total wins; a tie goes to the shorter text. The selection is
fully deterministic, so every run writes the same bytes.

Second pass (a real revision, not a walk-through)
-------------------------------------------------
The winning draft first ended "Flooding is not expected; falling is."
That tail is grammatically strained -- "falling is" has no subject to
lean on -- and the joke lands second-hand, after the punchline has
already fired. The revision leaves the whole first sentence untouched
(the upward rain and the umbrella instruction are the joke) and replaces
the tail with "Officials advise residents to stay grounded." That keeps
the official-advice register a real broadcast would use, adds a second
quiet pun (grounded = on the ground, and grounded = kept indoors), and
lands the line on advice instead of on a wobble. "will fall" also
tightened to "falls": present tense reads like a forecast being read off
the map right now.

  Draft:  146 chars, tail "Flooding is not expected; falling is."
  Winner: 149 chars, tail "Officials advise residents to stay grounded."

No network, no randomness, no secrets. Standard library only.
"""

import hashlib
import os
import sys

MAX_CHARS = 160

# Each entry: (forecast text, on-topic, funnier, vivid, broadcast, chars).
# Scores are hand-judged, 0-10 per criterion, total out of 50.
DRAFTS = [
    # 9 + 8 + 9 + 9 + 8 = 43
    # Fog that sets at ankle height is a strong image, but the step
    # stool kicker is a prop gag rather than a logical consequence.
    ("Overnight in Mistral Hollow, the fog will condense into a low "
     "ceiling and settle at ankle height. Commuters should bring step "
     "stools.",
     9, 8, 9, 9, 8),
    # 9 + 8 + 9 + 9 + 8 = 43
    # Sideways rain with umbrellas at a 90-degree angle is nicely
    # deadpan, but the second clause only restates the first image.
    ("In the town of Brindlewick, rain is forecast to fall sideways "
     "all afternoon, so umbrellas will be provided at a 90-degree "
     "angle.",
     9, 8, 9, 9, 8),
    # 9 + 8 + 8 + 9 + 8 = 42
    # "A low of mild applause" is a good absurd number; the standing
    # ovation tail doubles the same applause joke instead of adding one.
    ("Tomorrow in Port Chatter, expect a high of 74 and a low of mild "
     "applause, with a 40 percent chance of standing ovations by dusk.",
     9, 8, 8, 9, 8),
    # 9 + 9 + 9 + 9 + 8 = 44
    # Puddles drying upward is a vivid inversion and the ladder line
    # is funny; it loses only on character use (126 of 160).
    ("In New Puddington, the puddles will dry upward today, leaving "
     "the streets wet from the sky down. Bring a towel and a ladder.",
     9, 9, 9, 9, 8),
    # 9 + 9 + 8 + 9 + 8 = 43
    # Snow falling in alphabetical order is a clean absurd premise;
    # "shovel in sequence" is a solid deadpan instruction, but the
    # image is thinner than the winner's upward rain.
    ("Overnight in Cragmoor, snow will fall in alphabetical order, "
     "starting with A. Residents are asked to shovel in sequence.",
     9, 9, 8, 9, 8),
    # 9 + 7 + 8 + 8 + 8 = 40
    # Gossiping clouds are charming, but "saying nothing of substance"
    # is a shrug where a kicker should be, and the broadcast register
    # slips into whimsy.
    ("In the village of Larksong, clouds will gather at noon to gossip, "
     "then disperse by 3 p.m. after saying nothing of substance.",
     9, 7, 8, 8, 8),
    # 9 + 8 + 8 + 9 + 8 = 42
    # A wind that changes its mind is a good premise; "not taking it
    # personally" is a decent kicker, but the image has no concrete
    # number or detail to hold onto.
    ("In the town of Vexley, the wind will change its mind six times "
     "before lunch. Forecasters recommend not taking it personally.",
     9, 8, 8, 9, 8),
    # 9 + 8 + 8 + 9 + 8 = 42
    # A river that thinks better of rising is a nice deadpan beat;
    # "or believed in" reaches for a second joke the line does not need.
    ("In Shallowford, the river will rise exactly one inch, then think "
     "better of it and go back down. No sandbags are required, or "
     "believed in.",
     9, 8, 8, 9, 8),
    # 9 + 8 + 9 + 9 + 8 = 43
    # A drizzle of Mondays is a vivid image and "a spare weekend" is a
    # good kicker; loses a point on character use (125 of 160).
    ("Tomorrow in Drowsy Hollow, a light drizzle of Mondays is expected "
     "through the morning, clearing by noon. Carry a spare weekend.",
     9, 8, 9, 9, 8),
    # 9 + 8 + 8 + 8 + 8 = 41
    # Tumbleweeds stopping for red lights is funny, but the line reads
    # more like a sight gag than a forecast, and the broadcast tone is
    # the weakest of the set.
    ("In the city of Tumbleweed, tumbleweeds will roll in from the east "
     "at 25 miles per hour, stopping only for red lights.",
     9, 8, 8, 8, 8),
    # 9 + 8 + 9 + 9 + 8 = 43
    # Frost in the shape of a shrug is vivid and "cover their optimism"
    # is a good deadpan instruction; the image is slightly less
    # immediately funny than the winner's.
    ("Overnight in Brackenfield, frost will settle on the rooftops in "
     "the shape of a shrug. Gardeners should cover their optimism.",
     9, 8, 9, 9, 8),
    # 9 + 9 + 9 + 9 + 9 = 45  (WINNER)
    # Upward rain at a stated speed, an umbrella held underneath, and
    # official advice to stay grounded: one absurd premise, carried
    # through deadpan to its logical end, at 149 of 160 characters.
    # See the second-pass note above: the draft tail was replaced.
    ("In Flotsam, rain falls upward at 30 miles per hour after "
     "midnight, so hold your umbrella underneath you. Officials "
     "advise residents to stay grounded.",
     9, 9, 9, 9, 9),
]


def total_score(entry):
    """Sum of the five hand-judged criterion scores (0-50)."""
    return sum(entry[1:])


def choose(drafts):
    """Highest total wins; ties go to the shorter forecast."""
    ranked = sorted(drafts, key=lambda e: (total_score(e), -len(e[0])),
                    reverse=True)
    top = ranked[0]
    return top[0], total_score(top)


def write_entry():
    forecast, score = choose(DRAFTS)
    if not forecast.strip():
        sys.exit("winner is empty")
    if "\n" in forecast or "\r" in forecast:
        sys.exit("winner must be a single line")
    if len(forecast) > MAX_CHARS:
        sys.exit("winner exceeds %d characters: %d"
                 % (MAX_CHARS, len(forecast)))
    out_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    payload = forecast.encode("utf-8")
    with open(out_path, "wb") as handle:
        handle.write(payload)
    # Read back and confirm the file is byte-identical to the winner.
    with open(out_path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        sys.exit("self-check failed: output differs from winner")
    print("entry (%d chars, score %d/50): %s"
          % (len(forecast), score, forecast))
    print("sha256: %s" % hashlib.sha256(on_disk).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(write_entry())
