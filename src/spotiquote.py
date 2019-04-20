#!/usr/bin/env python3
# pylint: disable=bad-continuation
"""
Library containing the main functionality of Spotiquote
"""
import random
import json
import time
import re
import subprocess


def main(volume, memos_fpath, default_voice, valid_voices, after_num_plays):
    """
    Main wrapper containing retry logic of sadmute.

    Arguments:
        volume: int
            Volume to start Spotify with.
        memos_fpath: str | None
            File path to json file containing memos to say at the beginning of a muted
            advertisement.
        default_voice: str
            Default voice to say memos with.
        valid_voices: set(str)
            Set of allowed voices.
        after_num_plays: int | None
            Recite memo after an integer number of songs have completed. Completion of
            play is defined as reaching the last 5 seconds of a song. Must be at least
            one.
    """

    if memos_fpath:
        with open(memos_fpath, "r") as fptr:
            memos = (x.strip() for x in fptr if not x.startswith("#"))
            memos = [x for x in memos if x != ""]
    else:
        memos = []

    completed_songs = set()
    last_track_played = None
    memo_played = False
    non_zero_volume = spotify_volume()
    if non_zero_volume == 0:
        non_zero_volume = volume

    while True:
        stdout = subprocess.check_output(
            ["osascript", "src/spotiquote.scpt", str(non_zero_volume)]
        ).decode("utf-8")
        spotify_state = json.loads(stdout)

        if spotify_state["player_state"] == "stopped":
            continue

        if not spotify_state["advertisement"]:
            if memos and spotify_state["duration"] - spotify_state["position"] < 5:
                completed_songs |= set([spotify_state["track"]])
            elif (
                after_num_plays
                and last_track_played != spotify_state["track"]
                and len(completed_songs) >= after_num_plays
            ):
                spotify_playpause()
                _say_memo(random.choice(memos), valid_voices, voice=default_voice)
                spotify_playpause()
                completed_songs = set()
            memo_played = False
        elif not memo_played and memos:
            _say_memo(random.choice(memos), valid_voices, voice=default_voice)
            memo_played = True

        last_track_played = spotify_state["track"]
        if spotify_state["volume"] != 0:
            non_zero_volume = spotify_state["volume"]


def spotify_volume():
    """
    Returns volume Spotify is currently set at.

    Returns:
        int
            Volume as an integer.
    """
    volume = subprocess.check_output(
        ["osascript", "-e", 'tell Application "Spotify" to set info to sound volume']
    ).decode("utf-8")

    return int(volume)


def spotify_playpause():
    """
    Send playpause command to Spotify.
    """
    subprocess.Popen(["osascript", "-e", 'tell application "Spotify" to playpause'])


def _say_memo(memo, valid_voices, voice="alex"):
    """
    Says a memo for a user to reflect on.

    If `...` is present in the memo a pause is inserted. If a speaker is detected by the
    pattern [v=[a-z]*]

    Arguments:
        memo: str
            Memo to be read out loud to the user.
        valid_voices: set(str)
            List of supported voices for passing to `say` command.
        voice: str
            Voice to read memo in.

    """
    process = subprocess.Popen(["say", "-v", voice, "Memo."])
    time.sleep(2)

    speaker = re.compile(r"(\[v=[a-zA-Z]+\])")
    phrases = [x for x in speaker.split(memo) if x != ""]

    for phrase in phrases:
        new_speaker = speaker.search(phrase)
        if new_speaker:
            voice = new_speaker.group(1)[3:-1].lower()
            continue

        if voice not in valid_voices:
            process = subprocess.Popen(
                ["say", "Invalid voice requested. Skipping memo."]
            )
            process.wait()
            break

        for chunk in phrase.split("..."):
            process = subprocess.Popen(["say", "-v", voice, chunk])
            process.wait()
            time.sleep(1)
