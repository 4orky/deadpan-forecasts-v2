"""Deadpan Forecasts for Cities That Do Not Exist.

An entry for the make.fun bounty
u-coral-ibis-18-deadpan-forecasts-for-cities-that-do-151d4d8c
($2, winner take all). The script picks a single-line weather
forecast, 1-160 characters, for a city that does not exist, and
writes it to /output/entry.txt.

How the line was picked
-----------------------
Twelve forecasts were drafted by hand against the brief, then marked
0-10 on five points, listed here in the order the judge weights them:

  1. on-subject: a forecast for a city that does not exist, absurd
     yet believable (anything off-subject loses outright)
  2. funny on a first read: a deadpan twist, not a pile of random
     absurdity
  3. vivid: a concrete image, number or detail that makes the made-up
     city's weather feel real
  4. broadcast register: plain, confident, believable, the way a
     straight-faced meteorologist would read it aloud
  5. character use: tight and well paced across its 160 characters

The best total wins; when two lines tie, the shorter one wins. The
pick is fully deterministic, so every run writes identical bytes.
Before picking, every entry is checked: five marks, each 0-10, and a
single line within the limit, so a typo in the hand-entered marks
fails loudly instead of silently changing the winner.

The winning line was revised once, for real
--------------------------------------------
Its first draft closed with "Flooding is not expected; falling is."
That closing is grammatically strained -- "falling is" has no subject
to lean on -- and its joke arrives second-hand, after the punchline
has already fired. The revision keeps the whole opening sentence
exactly as it was (the upward rain and the umbrella instruction are
the joke) and swaps the tail for "Officials advise residents to stay
grounded." The new tail keeps the official-advice register a real
broadcast would use, adds a second quiet pun (grounded as in on the
ground, and grounded as in kept indoors), and ends the line on advice
instead of on a wobble. "will fall" was also tightened to "falls":
present tense reads like a forecast being read off the map right now.

  Draft:  146 characters, tail "Flooding is not expected; falling is."
  Winner: 149 characters, tail "Officials advise residents to stay grounded."

Standard library only. No network, no randomness, no secrets.
"""

from hashlib import sha256
from os import environ
from pathlib import Path

CHARACTER_LIMIT = 160

# Each forecast: the line, five hand-judged marks (0-10 each, in the
# order listed in the docstring above), and a short note on why it
# scored that way.
FORECASTS = [
    {
        # Marks 9 + 8 + 8 + 9 + 8 = 42.
        # Fog arriving on foot is a charming image, but "wave it
        # through" is a polite shrug where a kicker should be, and
        # the line never quite lands a second beat.
        "line": ("In Wobbleton, the fog will arrive on foot at 6 a.m. "
                 "and leave by bicycle at noon. Drivers are advised "
                 "to wave it through."),
        "marks": (9, 8, 8, 9, 8),
    },
    {
        # Marks 9 + 8 + 8 + 9 + 8 = 42.
        # "A low of mild suspicion" is a good absurd number, but the
        # raised-eyebrows tail only restates the suspicion joke.
        "line": ("Tomorrow in Bramblewick, expect a high of 71 and a "
                 "low of mild suspicion, with a 30 percent chance of "
                 "raised eyebrows by dusk."),
        "marks": (9, 8, 8, 9, 8),
    },
    {
        # Marks 9 + 9 + 9 + 9 + 8 = 44.
        # A wind pausing for a commercial break is a clean deadpan
        # premise with a precise timestamp; it loses only on
        # character use (114 of 160 leaves room unspent).
        "line": ("Overnight in Port Lull, the wind will pause for a "
                 "commercial break at 9 p.m. and return, slightly "
                 "louder, at 9:03."),
        "marks": (9, 9, 9, 9, 8),
    },
    {
        # Marks 9 + 8 + 8 + 9 + 8 = 42.
        # Clouds holding a meeting that reaches no conclusion is a
        # nice bureaucratic joke, but the image is thin: no number,
        # no concrete detail to hold onto.
        "line": ("In the village of Hushwick, clouds will gather at "
                 "noon to discuss the weather, then disperse by "
                 "3 p.m. having reached no conclusion."),
        "marks": (9, 8, 8, 9, 8),
    },
    {
        # Marks 9 + 8 + 9 + 9 + 8 = 43.
        # Garden furniture relocated to the next county is a vivid
        # image and the advice is properly deadpan; the joke is a
        # single beat stretched across a long line.
        "line": ("Highs in Tumbleford reach 68 today, with gusts "
                 "strong enough to relocate garden furniture. "
                 "Residents are asked to check the next county."),
        "marks": (9, 8, 9, 9, 8),
    },
    {
        # Marks 9 + 9 + 8 + 9 + 8 = 43.
        # A tide that apologises is a strong deadpan twist; the
        # second sentence is a decent kicker, but the image has no
        # concrete number in it.
        "line": ("In Brinewick, the tide will come in twice this "
                 "morning, apologise, and go back out. Beachgoers "
                 "should accept the apology."),
        "marks": (9, 9, 8, 9, 8),
    },
    {
        # Marks 9 + 9 + 9 + 9 + 9 = 45.  (WINNER)
        # Upward rain at a stated speed, an umbrella held
        # underneath, and official advice to stay grounded: one
        # absurd premise, carried through deadpan to its logical
        # end, at 149 of 160 characters. See the revision note in
        # the docstring: the draft tail was replaced.
        "line": ("In Flotsam, rain falls upward at 30 miles per hour after "
                 "midnight, so hold your umbrella underneath you. Officials "
                 "advise residents to stay grounded."),
        "marks": (9, 9, 9, 9, 9),
    },
    {
        # Marks 9 + 8 + 9 + 9 + 8 = 43.
        # Frost waiting politely on the doorstep is vivid and the
        # "invite it in" instruction is properly deadpan; the image
        # is slightly less immediately funny than the winner's.
        "line": ("Overnight in Cragmoor, the frost will arrive early "
                 "and wait politely on the doorstep until 7 a.m. "
                 "Residents should invite it in."),
        "marks": (9, 8, 9, 9, 8),
    },
    {
        # Marks 9 + 8 + 8 + 9 + 8 = 42.
        # An indecisive wind is a good premise, but "standing still"
        # is a shrug of an instruction, and the line has no concrete
        # number or detail to hold onto.
        "line": ("In Vexley, the wind will be indecisive all "
                 "afternoon, gusting from every direction at once. "
                 "Forecasters advise standing still."),
        "marks": (9, 8, 8, 9, 8),
    },
    {
        # Marks 9 + 9 + 8 + 9 + 8 = 43.
        # A river running backwards "just to see" is a clean absurd
        # premise and the anglers' instruction lands; the image is
        # thinner than the winner's upward rain.
        "line": ("In Shallowford, the river will run backwards for an "
                 "hour at dawn, just to see. Anglers are advised to "
                 "face the other way."),
        "marks": (9, 9, 8, 9, 8),
    },
    {
        # Marks 9 + 8 + 8 + 9 + 8 = 42.
        # "A low of polite silence" is a good absurd number, but the
        # small-talk tail doubles the same social joke instead of
        # adding one.
        "line": ("Tomorrow in Port Chatter, expect a high of 74 and a "
                 "low of polite silence, with a 60 percent chance of "
                 "small talk by evening."),
        "marks": (9, 8, 8, 9, 8),
    },
    {
        # Marks 9 + 9 + 9 + 9 + 8 = 44.
        # A flurry of misplaced umbrellas is vivid and the plows
        # line is a clean deadpan kicker; it loses only on character
        # use (123 of 160).
        "line": ("In Kettleford, expect a light flurry of misplaced "
                 "umbrellas, accumulating two inches by dawn. The "
                 "plows have been notified."),
        "marks": (9, 9, 9, 9, 8),
    },
]


def total_marks(forecast):
    """Add up one forecast's five hand-judged marks (0-50)."""
    return sum(forecast["marks"])


def validate_forecasts(forecasts):
    """Fail loudly on a typo in the hand-entered marks.

    Revision, found by running the first draft: nothing checked the
    marks before selection, so a single mistyped mark (a 19 instead
    of a 9, a four-tuple instead of five) would silently change the
    winner. Every entry must now carry exactly five marks, each 0-10,
    and a single line within the character limit, or the program
    stops before picking anything.
    """
    for forecast in forecasts:
        marks = forecast["marks"]
        if len(marks) != 5 or any(m < 0 or m > 10 for m in marks):
            raise SystemExit("bad marks on entry: %r" % (forecast["line"][:40],))
        line = forecast["line"]
        if not line.strip() or "\n" in line or len(line) > CHARACTER_LIMIT:
            raise SystemExit("bad line on entry: %r" % (line[:40],))


def pick_winner(forecasts):
    """Return (line, total) of the best forecast.

    Highest total wins; a tie goes to the shorter line. The first
    entry wins any tie that survives both rules, so the result is
    deterministic.
    """
    champion = None
    for forecast in forecasts:
        total = total_marks(forecast)
        if champion is None:
            champion = (forecast["line"], total)
            continue
        champion_line, champion_total = champion
        if total > champion_total or (
            total == champion_total
            and len(forecast["line"]) < len(champion_line)
        ):
            champion = (forecast["line"], total)
    return champion


def publish(line, total):
    """Check the winning line, write it out, verify the bytes."""
    if not line.strip():
        raise SystemExit("winner is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("winner must be a single line")
    if len(line) > CHARACTER_LIMIT:
        raise SystemExit(
            "winner exceeds %d characters: %d" % (CHARACTER_LIMIT, len(line))
        )
    target = Path(environ.get("OUTPUT_PATH", "/output/entry.txt"))
    if target.parent != Path("."):
        target.parent.mkdir(parents=True, exist_ok=True)
    encoded = line.encode("utf-8")
    target.write_bytes(encoded)
    if target.read_bytes() != encoded:
        raise SystemExit("self-check failed: output differs from winner")
    print("winner (%d chars, %d/50): %s" % (len(line), total, line))
    print("sha256: %s" % sha256(encoded).hexdigest())
    return 0


def entry_point():
    validate_forecasts(FORECASTS)
    line, total = pick_winner(FORECASTS)
    return publish(line, total)


if __name__ == "__main__":
    raise SystemExit(entry_point())
