#
#  Subtitle time shift implementation.
#
#  Copyright (c) 2016, Norman Patrick
#
#  Permission to use, copy, modify, and distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
import re
import argparse

def extractTimes(s):
    isTime = False
    tStart = tEnd = (0,0,0,0)
    m = re.match(r'\s*(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)', s)
    if m:
        h0, m0, s0, ms0, h1, m1, s1, ms1 = [int(x) for x in m.groups()]
        isTime = True
        tStart = (h0, m0, s0, ms0)
        tEnd = (h1, m1, s1, ms1)
    return isTime, tStart, tEnd

def timesToString(tStart, tEnd):
    h0, m0, s0, ms0 = tStart
    h1, m1, s1, ms1 = tEnd
    return "{:02d}:{:02d}:{:02d},{:03d} --> {:02d}:{:02d}:{:02d},{:03d}".format(
        h0, m0, s0, ms0, h1, m1, s1, ms1)

def timePlusDelta(t0, delta):
    hh, mm, ss, ms = t0
    seconds = (hh * 60 * 60) + (mm * 60) + ss
    t1 = seconds + delta
    hours = t1 / (60 * 60)
    x = t1 - (hours * 60 * 60)
    mins = x / 60
    sec = x % 60
    return (hours, mins, sec, ms)

def testTimePlusDelta(t0, delta):
    print "t0:", t0, "delta:", delta
    t1 = timePlusDelta(t0, delta)
    print "t1", t1

def testExtractTime(s):
    print "input:", s
    isTime, tStart, tEnd = extractTimes(s)
    print isTime, tStart, tEnd
    print timesToString(tStart, tEnd) if isTime else ""

def testFn2():
    text = """
      3
      00:01:05,220 --> 00:01:08,121
      ~ You are Mister...
      ~ Perrin. Francois Perrin.

      4
      00:01:10,120 --> 00:01:13,465
      Mr. de Blenac, Mr. Francois Perrin is here.

      5
      00:01:13,820 --> 00:01:15,822
      A moment, please.

      6
      00:02:36,020 --> 00:02:40,821
      ~ Mr. de Blenac is expecting you.
      ~ Thank you.
    """
    [testExtractTime(s) for s in text.splitlines()]

def testFn1():
    vector = [
        ((00,01,10,100), 16),
        ((00,00,49,201), 16),
        ((01,27,47,101), 16),
        ((00,01,10,50), -16),
        ((00,00,49,800), -16),
        ((01,27,47,197), -16),
    ]
    [testTimePlusDelta(t0, delta) for t0, delta in vector]

def allTests():
    testFn1()
    testFn2()

def shiftTime(inFile, outFile, plusDelta):
    with open(inFile, "r") as fin, open(outFile, "w") as fout:
        for l in fin.readlines():
            isTime, tStart, tEnd = extractTimes(l)
            if isTime:
                fout.write(timesToString(timePlusDelta(tStart, plusDelta),
                                         timePlusDelta(tEnd, plusDelta)))
                fout.write("\r\n")
            else:
                fout.write(l)

def main():
    parser = argparse.ArgumentParser(
        description='Shift subtitle texts by a few seconds')
    parser.add_argument('-d', '--delta', type=int, default=0,
        help="Shift all subtitle texts by a fixed amount +/- seconds")
    parser.add_argument('-i', '--input-filename', default=None,
                        help="Input srt filename")
    parser.add_argument('-o', '--output-filename', default=None,
                        help="Output file to create")
    args = parser.parse_args()

    rc = True
    inFile = args.input_filename
    outFile = args.output_filename
    if not inFile:
        print "  + Please provide an input filename"
        rc = False

    if not outFile:
        print "  + Please provide an output filename"
        rc = False

    if not args.delta:
        print "  + Please provide a non-zero (-ve or +ve) delta value in seconds"
        rc = False

    if not rc:
        print "Error: incorrect parameters provided"
        return

    if not os.path.exists(inFile):
        print "  + Input file {} does not exist".format(inFile)
        return

    if os.path.exists(outFile):
        print "  + Output file {} already exists!".format(outFile)
        choice = raw_input("Overwrite? (y/N)").lower()
        if choice != "y":
            return

    print "Time-shifting....{} => {}".format(inFile, outFile)
    shiftTime(inFile, outFile, args.delta)
    print "Done!, check {} for results".format(outFile)
    return


if __name__ == '__main__':
    main()
