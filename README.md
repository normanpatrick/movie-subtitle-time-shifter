> movie-subtitle-time-shifter: A minimalistic SRT file time shifter for all sub-titles

## What is it

This is a result of about 1 hour work from concept to hacking. I had a non-English
movie and a seperate .srt file for the English sub-titles. Unfortunately the text
popped up about 16 seconds after the speech on the screen, which is annoying and
also it is hard to follow who is saying which part of the text.

This code allows the text timestamps to shift forward or backward as specified in
the commandline.

## Installation

Make sure the following is/are installed:

* Python 2.7x

This code has been tested in OSX, but it does not have any OS specific dependency, it
should work fine on Linux and Windows variety.

## Usage

```bash
python shifter.py -h
usage: shifter.py [-h] [-d DELTA] [-i INPUT_FILENAME] [-o OUTPUT_FILENAME]

Shift subtitle texts by a few seconds

optional arguments:
  -h, --help            show this help message and exit
  -d DELTA, --delta DELTA
                        Shift all subtitle texts by a fixed amount +/- seconds
  -i INPUT_FILENAME, --input-filename INPUT_FILENAME
                        Input srt filename
  -o OUTPUT_FILENAME, --output-filename OUTPUT_FILENAME
                        Output file to create
```

Example commands:
```bash
# Move all sub-titles by -12 seconds. i.e. move back
python shifter.py -i input.srt -o out_move_back_12_sec.srt -d -12
Time-shifting....input.srt => out_move_back_12_sec.srt
Done!, check out_move_back_12_sec.srt for results

# Move sub-titles by 10 seconds ahead in the video
python shifter.py -i input.srt -o out_move_forward_10_sec.srt -d 10
Time-shifting....input.srt => out_move_forward_10_sec.srt
Done!, check out_move_forward_10_sec.srt for results
```

## Unit Tests

In order to run tests you will have to invoke the function listed below. Unless you
are modifying the code, there is no need to execute these.

```python
def allTests():
    testFn1()
    testFn2()
```

## TODO

1. Error checking for badly formatted files
1. Allow user to specify the delta in milliseconds instead of seconds

## License

MIT
