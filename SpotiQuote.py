#!/usr/bin/env python3
# pylint: disable=pointless-string-statement
"""
SpotiQuote: An automatic ad silencer combined with spottily played quotes.

Spotify is queried by an AppleScript to report its status and when found to be
presenting an advertisement, automatically muted. Once an advertisement concludes the
volume is set back to its previous level. During muted sessions a quote is read back
to the reader. Readings can be extended passed quotes and in general are referred to
as memos to illustrate this capability.

Additional functionality is provided for listening to spaced repetition of quotes
between songs defined by some user interval.
"""
import argparse
import fcntl
import os
import subprocess
import sys

from src import spotiquote

BOLD, RED, GREEN, END = ("\033[{x}m".format(x=x) for x in (1, 91, 32, 0))


def spotify_running():
    """
    Determines if Spotify is currently running.

    Returns
        bool:
            True if Spotify is running False otherwise including the case where
            Spotify has not been installed.
    """
    stdout = (
        subprocess.check_output(["osascript", "-e", 'application "Spotify" is running'])
        .decode("utf-8")
        .strip()
    )

    return stdout == "true"


def parse_arguments():
    """
    Main CLI for interfacing with SpotiQuote.

    Returns:
        argparse.Namespace
            Argparse namespace containg CLI inputs.

    """
    parser = argparse.ArgumentParser(
        description=(
            "SpotiQuote: An automatic ad silencer combined with spottily played quotes."
            " Spotify is queried by an AppleScript to report its status and when found"
            " to be presenting an advertisement, automatically muted. Once the an"
            " advertisement concludes the volume is set back to its previous level."
        )
    )

    parser.add_argument(
        "--volume",
        type=int,
        default=80,
        dest="volume",
        help="Integer value between 0 and 100 to start Spotify at.",
    )

    parser.add_argument(
        "--memos",
        type=str,
        default=None,
        dest="memos",
        help=(
            "File path to json file containing memos to say at the beginning of a muted"
        ),
    )

    parser.add_argument(
        "--voice",
        type=str,
        default="Alex",
        dest="voice",
        help="Default voice to read memos in",
    )

    parser.add_argument(
        "--after_num_plays",
        type=int,
        default=None,
        dest="after_num_plays",
        help=(
            "Recite memo after an integer number of songs have completed. Completion"
            " of play is defined as reaching the last 5 seconds of a song. Must be at"
            " least one."
        ),
    )

    return parser.parse_args()


def assert_argument_vals(args, valid_voices):
    """
    Various asserts to enforce CLI arguments passed are valid.

    Arguments:
        args: argparse.Namespace
            Argparse namespace containg CLI inputs.
        valid_voices: set(str)
            Valid voices installed on Mac for `say` CLI function.
    """
    assert (
        args.volume >= 0 and args.volume <= 100
    ), "Please provide a volume between [0, 100]."

    assert not args.memos or (
        args.memos and os.path.exists(args.memos)
    ), "File path to memos does not exist."

    assert not args.after_num_plays or (
        args.after_num_plays >= 1
    ), "Cannot play more than after every completed song."

    assert args.voice.lower() in valid_voices, (
        "Voice passed is not considered valid. Please consult:"
        "\n\t'say -v \"?\"'"
        "\nfor a list of valid voices and corresponding languages"
    )


if __name__ == "__main__":
    """
    CLI for parsing and validating values passed to SpotiQuote.

    Writes a locked pid file to prevent multiple instances of SpotiQuote from running
    at the same time. Spotify is required to be running before SpotiQuote is run.
    """
    if not spotify_running():
        print(RED + "Spotify must be running to start SpotiQuote." + END)
        sys.exit(0)

    ARGS = parse_arguments()
    STDOUT = subprocess.check_output(["say", "-v", "?"]).decode("utf-8")
    VALID_VOICES = set(x.rsplit(" ")[0].lower() for x in STDOUT.split("\n")[:-1])

    assert_argument_vals(ARGS, VALID_VOICES)

    PID_FILE = "spotiquote.pid"
    FPTR = open(PID_FILE, "w")

    try:
        fcntl.lockf(FPTR, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print(
            RED
            + "Another instance of Spotiquote is already running in the background"
            + "\nPlease find corresponding pid, terminate and try again"
            + END
        )
        sys.exit(0)

    try:
        print(BOLD + GREEN + "Starting SpotiQuote" + END)
        spotiquote.main(
            ARGS.volume,
            ARGS.memos,
            ARGS.voice.lower(),
            VALID_VOICES,
            ARGS.after_num_plays,
        )
    except subprocess.CalledProcessError:
        if not spotify_running():
            print(RED + "Spotify no longer running, terminating SpotiQuote." + END)
            sys.exit(0)
    except:
        raise
    finally:
        fcntl.flock(FPTR, fcntl.LOCK_UN)
        FPTR.close()
        os.remove(PID_FILE)
