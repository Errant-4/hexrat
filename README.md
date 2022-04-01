HexRat is currently a prototype and is provided as is. It may change, suffer feature creep, or never be updated again with little warning

It worked on my end (under both windows and Linux, though some features are disabled on Linux. mostly VA related so you won't miss them) and I consider it generally safe for ratting but YOU are responsible if you use this and it accidentally goofs up, or if you miss something important because it was filtered

It should not throw errors at you anymore, if it does please let me know

# Installation

1. When you install HexChat, select the Python Interface for install as well. If you already installed hexchat but not the python interface, run the installer again to add it

2. You will need additional Python modules: "pyperclip" and "pygame"

3. ~~Open hexrat.py and change the path and/or names for the sound files you want to use for the designated event types~~ Put hexrat.conf in /Hexchat/ and open it to edit the file names for all listed sound effects to whatever sounds you have/want to use. You can also change where hexrat will look for these files, the default is HexChat/sounds/ folder

4. put hexrat.py in Hexchat/addons   and hexrat will automatically load on hexchat startup

5. Optional: put hexrat-loader.py in Hexchat/addons if you want to be able to refresh/load hexrat with a single command (/hr). You shouldn't need this for normal use

# Known issues: 

it will throw errors if it's left running while the desktop is locked, because it won't be able to reach the clipboard

When it's cutting Mecha or Quit-messages short, it's set for the exact font and window size I'm using, results may vary

It's tuned for a dark color scheme and will probably be barely eligible on a white background. If you use a dark colorscheme that's not exactly like mine, or if your text events are not exactly like mine, the appearance will not be fully consistent You can use the provided colors.conf and pevents.conf

If you want to use it for console or Ody you will have to change the sound trigger conditions in hexrat.py around lines 260-300, I set them to use ssk (skip)
