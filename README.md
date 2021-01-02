# lss tools

Tools to parse and analyze LiveSplit `.lss` files. At the moment it supports only command, `deviation`

## deviation
Calculates [standard deviation](https://en.wikipedia.org/wiki/Standard_deviation) on each segment history to figure out which splits are the least consistent. You can specify lower bound on the attempt id, so that you can not account for very old segment times.

### deviation example
In [example-splits/4ms.lss](./example-splits/4ms.lss), we find that attempt 171 is the beginning of a recent set of attempts:
```xml
    <Attempt id="170" started="11/15/2020 05:53:01" isStartedSynced="True" ended="11/15/2020 05:56:00" isEndedSynced="True" />
    <Attempt id="171" started="12/22/2020 14:35:54" isStartedSynced="True" ended="12/22/2020 14:40:47" isEndedSynced="True" />
```

So, we are interested in how inconsistent we have been since then:
```
$ ./src/lss.py deviation ./example-splits/4ms.lss --minattemptid 171
Mean           Median         Deviation      Gold           Split Name
00:00:29.240   00:00:26.357   00:00:06.687   00:00:25.320   Aspid Arena
00:01:20.848   00:01:23.652   00:00:05.703   00:01:13.138   Mawlek
00:00:32.208   00:00:30.440   00:00:03.983   00:00:29.934   Grub 2
00:00:27.295   00:00:27.315   00:00:03.245   00:00:22.603   Grub 5
00:01:01.773   00:01:02.115   00:00:02.565   00:00:58.392   Gruz Mother
00:00:51.717   00:00:51.971   00:00:02.285   00:00:48.696   Grub 3
00:00:37.165   00:00:37.335   00:00:01.425   00:00:35.038   Shard 2
00:01:12.335   00:01:12.369   00:00:01.330   00:01:09.817   Dirtmouth
00:00:20.408   00:00:20.129   00:00:00.998   00:00:18.911   Grub 4
00:00:48.470   00:00:48.472   00:00:00.742   00:00:46.491   Shard 3
00:00:35.071   00:00:34.858   00:00:00.614   00:00:33.533   Grub 1
00:00:21.781   00:00:21.635   00:00:00.610   00:00:19.863   Shard 4
00:00:10.054   00:00:09.914   00:00:00.455   00:00:09.449   Shard 1

```

This tells us that, when we do segment practice, we should focus on `Aspid Arena`*, `Grub 1`, and `Mawlek`.

*_In these splits, `Aspid Arena` includes a hazard respawn after the acid grub. Missing the respawn loses a lot of time._

⚠ **If you have recently added splits in the middle of other splits, be sure `minattemptid` is after that point**
