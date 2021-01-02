[![Build Status](https://travis-ci.org/slaurent22/lss-tools.svg?branch=main)](https://travis-ci.org/slaurent22/lss-tools)

# lss tools

Tools to parse and analyze LiveSplit `.lss` files. At the moment it supports only command, `deviation`

## deviation
Calculates [standard deviation](https://en.wikipedia.org/wiki/Standard_deviation) on each segment history to figure out which splits are the least consistent. You can specify lower bound on the attempt id, so that you can not account for very old segment times.

```
$ ./src/lss.py deviation --help
usage: lss.py deviation [-h] [--comparison {GameTime,RealTime}]
                        [--minattemptid MINATTEMPTID]
                        [--zscore-cutoff ZSCORE_CUTOFF]
                        splits_file

positional arguments:
  splits_file           The .lss splits file to analyze

optional arguments:
  -h, --help            show this help message and exit
  --comparison {GameTime,RealTime}
                        Time comparison to analyze. Default: GameTime
  --minattemptid MINATTEMPTID
                        Minimum attempt id to analyze. Drops data from
                        attempts below this id.
  --zscore-cutoff ZSCORE_CUTOFF
                        Z-Score outside of which to drop outliers.
```

### deviation example
In [example-splits/4ms.lss](./example-splits/4ms.lss), we find that attempt 171 is the beginning of a recent set of attempts:
```xml
    <Attempt id="170" started="11/15/2020 05:53:01" isStartedSynced="True" ended="11/15/2020 05:56:00" isEndedSynced="True" />
    <Attempt id="171" started="12/22/2020 14:35:54" isStartedSynced="True" ended="12/22/2020 14:40:47" isEndedSynced="True" />
```

So, we are interested in how inconsistent we have been since then:
```bash
# keep outliers:
$ ./src/lss.py deviation ./example-splits/4ms.lss --minattemptid 171 | head -n 4
Mean           Median         Deviation      Gold           Split Name
00:00:29.240   00:00:26.357   00:00:06.687   00:00:25.320   Aspid Arena
00:00:36.560   00:00:34.905   00:00:05.799   00:00:33.533   Grub 1
00:01:20.848   00:01:23.652   00:00:05.703   00:01:13.138   Mawlek

# remove outliers:
$ ./src/lss.py deviation ./example-splits/4ms.lss --minattemptid 171 --zscore-cutoff 3 | head -n 4
Mean           Median         Deviation      Gold           Split Name
00:00:29.240   00:00:26.357   00:00:06.687   00:00:25.320   Aspid Arena
00:01:20.848   00:01:23.652   00:00:05.703   00:01:13.138   Mawlek
00:00:32.208   00:00:30.440   00:00:03.983   00:00:29.934   Grub 2
```

This tells us that, when we do segment practice, we should focus on `Aspid Arena`* and `Mawlek`. When we keep outliers, we also find `Grub 1` to be very inconsistent. When we remove outliers beyond z-score `3`, we find `Grub 2` much more inconsistent.

*_In these splits, `Aspid Arena` includes a hazard respawn after the acid grub. Missing the respawn loses a lot of time._

⚠ **If you have recently added splits in the middle of other splits, be sure `minattemptid` is after that point**
