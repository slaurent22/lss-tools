[![Build Status](https://travis-ci.org/slaurent22/lss-tools.svg?branch=main)](https://travis-ci.org/slaurent22/lss-tools)

# lss tools

Tools to parse and analyze LiveSplit `.lss` files. At the moment it supports only command, `deviation`

## deviation
Calculates [standard deviation](https://en.wikipedia.org/wiki/Standard_deviation) on each segment history to figure out which splits are the least consistent. You can specify lower bound on the attempt id, so that you can not account for very old segment times.

```
$ ./main.py deviation --help
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

### deviation example: 4 mask shards
In [example-splits/4ms.lss](./example-splits/4ms.lss), we find that attempt 171 is the beginning of a recent set of attempts:
```xml
<Attempt id="170" started="11/15/2020 05:53:01" />
<Attempt id="171" started="12/22/2020 14:35:54" />
```

So, we are interested in how inconsistent we have been since then:
```bash
# keep outliers:
$ ./main.py deviation ./example-splits/4ms.lss --minattemptid 171 | head -n 4
Mean           Median         Deviation      Gold           Gold Z-Score   Split Name
00:00:29.240   00:00:26.357   00:00:06.687   00:00:25.320   -0.59          Aspid Arena
00:00:36.560   00:00:34.905   00:00:05.799   00:00:33.533   -0.52          Grub 1
00:01:20.848   00:01:23.652   00:00:05.703   00:01:13.138   -1.35          Mawlek


# remove outliers:
$ ./main.py deviation ./example-splits/4ms.lss --minattemptid 171 --zscore-cutoff 3
Mean           Median         Deviation      Gold           Gold Z-Score   Split Name
00:00:29.240   00:00:26.357   00:00:06.687   00:00:25.320   -0.59          Aspid Arena
00:01:20.848   00:01:23.652   00:00:05.703   00:01:13.138   -1.35          Mawlek
00:00:32.208   00:00:30.440   00:00:03.983   00:00:29.934   -0.57          Grub 2
00:00:27.295   00:00:27.315   00:00:03.245   00:00:22.603   -1.45          Grub 5
00:01:01.773   00:01:02.115   00:00:02.565   00:00:58.392   -1.32          Gruz Mother
00:00:51.717   00:00:51.971   00:00:02.285   00:00:48.696   -1.32          Grub 3
00:00:37.165   00:00:37.335   00:00:01.425   00:00:35.038   -1.49          Shard 2
00:01:12.335   00:01:12.369   00:00:01.330   00:01:09.817   -1.89          Dirtmouth
00:00:20.408   00:00:20.129   00:00:00.998   00:00:18.911   -1.5           Grub 4
00:00:48.470   00:00:48.472   00:00:00.742   00:00:46.491   -2.67          Shard 3
00:00:35.071   00:00:34.858   00:00:00.614   00:00:33.533   -2.5           Grub 1
00:00:21.781   00:00:21.635   00:00:00.610   00:00:19.863   -3.14 !!!      Shard 4
00:00:10.054   00:00:09.914   00:00:00.455   00:00:09.449   -1.33          Shard 1
```

This tells us that, when we do segment practice, we should focus on `Aspid Arena`* and `Mawlek`. When we keep outliers, we also find `Grub 1` to be very inconsistent. When we remove outliers beyond z-score `3`, we find `Grub 2` much more inconsistent.

A low `Gold Z-Score` means that we usually perform pretty close to our gold. When given `--zscore-cutoff 3`, we are also warned that our gold for `Shard 4` is an outlier. We may wish to keep this in mind when comparing to golds, or even consider removing the gold there.

*_In these splits, `Aspid Arena` includes a hazard respawn after the acid grub. Missing the respawn loses a lot of time._

### deviation example: all skills
We will use `--minattemptid 38` to remove 3 months of rust:

```xml
<Attempt id="37" started="09/12/2020 18:11:17" />
<Attempt id="38" started="12/22/2020 22:18:00" />
```

Finding outlier golds:
```bash
$ ./main.py deviation ./example-splits/allskills.lss --minattemptid 38 --zscore-cutoff 3
Mean           Median         Deviation      Gold           Gold Z-Score   Split Name
# ...
00:02:22.272   00:02:22.084   00:00:06.771   00:01:59.263   -3.4  !!!      Great Slash
```

## deviation caveat

⚠ **If you have recently added splits in the middle of other splits, be sure `minattemptid` is after that point**
