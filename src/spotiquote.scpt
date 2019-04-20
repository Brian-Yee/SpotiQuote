on run argv
    set argVolume to (item 1 of argv) as integer

    tell application "Spotify"
        set playerState to player state as string
        set currentVolume to sound volume

        if playerState is equal to "stopped" then
           set trackName to ""
           set trackArtist to ""
           set trackDuration to 0
           set trackPosition to 0
        else
           set trackName to name of current track
           set trackArtist to artist of current track
           set trackDuration to (duration of current track / 1000)
           set trackPosition to player position
        end if

        set advertisement to trackName equal ""
        set advertisement to advertisement or trackName equal "Advertisement"
        set advertisement to advertisement or trackName equal "Spotify"

        -- if in ad state ensure volume is muted
        if advertisement then
            if currentVolume is not equal to 0 then
                set sound volume to 0
            end if
        else
            if currentVolume is equal to 0 then
                set sound volume to argVolume
            end if
        end if

        -- build json of current Spotify state
        set info to "{" 
        set info to info & "\"track\": \"" & trackName & "\""
        set info to info & ", \"artist\": \"" & trackArtist & "\""
        set info to info & ", \"player_state\": \"" & playerState & "\""
        set info to info & ", \"duration\": " & trackDuration
        set info to info & ", \"position\": " & trackPosition
        set info to info & ", \"volume\": " & currentVolume
        set info to info & ", \"advertisement\": " & advertisement
        set info to info & "}" 
        
    end tell

    return info
end run
