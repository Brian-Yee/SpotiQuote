# SpotiQuote

----

SpotiQuote is a Python3 CLI automatic ad silencer for Spotify on Mac.
To fill in the silence a user can have random quotes/memos read to them by Mac's `say` command.
Additionally one can have quotes/memos read to them after every `n` played songs, where a song played is defined as reaching the last `5` seconds.

# Installation

----

## Manual installation

Simply clone down the repo and test it out with the `Makefile` to get started. 
Dependencies for running are all standard `python` install modules.
For development [`black`](https://github.com/ambv/black) and [`pylint`](https://github.com/PyCQA/pylint).

# Overview

----

Output of `make help` is

```
help             Display this message.
run.             Run SpotiQuote example in foreground with:
  default          defaults (no memos, ads silenced).
  programmer       programmer adages read at the beginning of silenced ads.
  japanese         Japanese word learning example.
  buddhism         Buddhist quote after every played (reached last 5s) song.
  cognitive        Cognitive bias definitions after every played (reached last 5s) song.
                     - Memo file of this example uses "..." to space defitions/terms.
test             Run testing suite.
clean            Clean repository.
deps             Install dependencies.
```

Output of `python SpotiQuote.py -h`

```
usage: SpotiQuote.py [-h] [--volume VOLUME] [--memos MEMOS] [--voice VOICE]
                     [--after_num_plays AFTER_NUM_PLAYS]

SpotiQuote: An automatic ad silencer combined with spottily played quotes.
Spotify is queried by an AppleScript to report its status and when found to be
presenting an advertisement, automatically muted. Once the an advertisement
concludes the volume is set back to its previous level.

optional arguments:
  -h, --help            show this help message and exit
  --volume VOLUME       Integer value between 0 and 100 to start Spotify at.
  --memos MEMOS         File path to json file containing memos to say at the
                        beginning of a muted
  --voice VOICE         Default voice to read memos in
  --after_num_plays AFTER_NUM_PLAYS
                        Recite memo after an integer number of songs have
                        completed. Completion of play is defined as reaching
                        the last 5 seconds of a song. Must be at least one.
```

# Memo Formatting

----

Memo files should put one memo per line and use `...` to enforce a `2` second pause.
A speaker can be selected by writing `[v={SPEAKER}]` where `{SPEAKER}` is a case-insensitive name.
To see a list of speakers available on your machine run `say -v "?"` in a command.
Different speakers are optimized for different languages.
For example, `Kyoko` is optimized for Japanese while `samantha` is optimized for US accented english.
Thus a file to used space repetition looks like.

```
[v=kyoko] ありがとうございます... [v=samantha] Thank you...
[v=kyoko] お願いします... [v=samantha] Please...
[v=kyoko] すみません... [v=samantha] Excuse me...
```

If you develop feelings for a speaker like 2013 Joaquin Phoenix in Spike Jonze's [Her](https://en.wikipedia.org/wiki/Her_(film)) instead of writing the speaker at the start of every line one can simply use the `--voice` flag to set a default speaker. 
