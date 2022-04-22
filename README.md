HexRat is currently a prototype and is provided as is. It may change, suffer feature creep, or never be updated again with little warning

It worked on my end (under both windows and Linux, though some features are disabled on Linux. mostly VA related so you won't miss them) and I consider it generally safe for ratting but YOU are responsible if you use this and it accidentally goofs up, or if you miss something important because it was filtered

It should not throw errors at you anymore, if it does please let me know

# Features

Custom-designed locally grown fully organic artisanal color scheme somewhat inspired by Elite: Dangerous

Automatically copies the System to the clipboard from ratsignals

Can quickly start tracking a specific case and pull the System to the clipboard

Adss case number prefixes to all known client nicks
In Dispatch mode, also adds a prefix for the platform

Shortens and semi-hides most Mecha messages in #fuelrats

Shortens quit messages (except for Bans) in #fuelrats

Custom highlights for your tracked client, the dispatcher, prep, jump calls and case reports, standdowns, and other things
Audio cues for ratsignals, preps, jump calls, stdn and hatsignals

Different audio alerts for standard and CR cases, as well as cases not on your chosen platform(s) (in Rat mode. Dispatch mode alerts are the same for all platforms)

An example custom rule to give specific users in ratchat a specific color so they are exactly as visible as you want

Everything else I forgot or neglected to list

# Installation

1. When you install HexChat, select the Python Interface for install as well. If you already installed hexchat but not the python interface, run the installer again to add it

2. You will need additional Python modules: "pyperclip" and "pygame"

3. Put the sounds in Hexchat/sounds. Put hexrat.conf in /Hexchat/ and edit any settings you want to change (such as your Platform)

4. put hexrat.py in Hexchat/addons   and hexrat will automatically load on hexchat startup

5. Optional: put hexrat-loader.py in Hexchat/addons if you want to be able to refresh/load hexrat with a single command (/hr). You shouldn't need this for normal use

# Known issues:

Several things are sent to #ratchat as a notification, and will throw ugly errors if you are not in #ratchat when you try to use them

~~it will throw errors if it's left running while the desktop is locked, because it won't be able to reach the clipboard~~

When it's cutting Mecha or Quit-messages short, it's set for the exact font and window size I'm using, results may vary

It's tuned for a dark color scheme and will probably be barely eligible on a white background. If you use a dark colorscheme that's not exactly like mine, or if your text events are not exactly like mine, the appearance will not be fully consistent You can use the provided colors.conf and pevents.conf

~~If you want to use it for console or Ody you will have to change the sound trigger conditions in hexrat.py around lines 260-300, I set them to use ssk (skip)~~


