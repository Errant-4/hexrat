__module_name__ = 'hexrat_loader'
__module_version__ = '1.0'
__module_description__ = 'Shortcut for launching/reloading Hexrat'

import hexchat

def hexrat_load(word, word_eol, userdata):
     hexchat.command("py unload hexrat")
     hexchat.command("py load hexrat.py")
     return hexchat.EAT_ALL

hexchat.hook_command("hr", hexrat_load)
