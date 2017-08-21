## Braille

> ASCII art is simply not precise enough
- The New York Times

The Braille character set in unicode provides more granularity over full-character ascii art
by decomposing a full character into a 2 by 4 set of dots, resulting in twice (quadruple) the 
horizontal (vertical) precision.

Right now, there are two features
* time series/bar plotting: a list like [1,2,3,4,5] gets plotted sequentially
* histogramming: a list like [1,2,3,4,5] gets turned into a frequency histogram, in the true sense of "histogram" (not just drawing bars on a regular x-y plot and calling it a histogram)

## Installation

It's a single file.

(Note that if you're using the histogram functionality, you need to have `numpy` installed.)

## Examples

N.B.: Characters seem to get shifted on asciinema, but they look perfect in a few terminals that I've tried. Trust me.

Try `python braille.py --example_hist` or `python braille.py --example_timeseries` to see some examples.
[![examples](https://asciinema.org/a/PfyL2Lq5BRZhOxQgQVu0PSxDR.png)](https://asciinema.org/a/PfyL2Lq5BRZhOxQgQVu0PSxDR?autoplay=1)

You can also pipe data via
```
seq 1 100 | ./braille.py
```
to get a sequential bar graph, or 
```
# central limit theorem: add 3 flat random numbers to get a pretty gaussian distribution
# -f forces the script to make a frequency histogram, rather than a time series by default
for i in `seq 1 10000`; do echo $((RANDOM + RANDOM + RANDOM)); done | ./braille.py -f
```
to get a gaussian histogram.

Or for full control in python,
```python
import random
import braille

# make a histogram with two flat peaks
# binning is automatic unless nbins is specified
vals = [random.random()-1.5 for _ in range(500)]
vals += [random.random()+1.5 for _ in range(500)]
painter = braille.Painter()
painter.draw(braille.make_hist(vals, nbins=25))
```
