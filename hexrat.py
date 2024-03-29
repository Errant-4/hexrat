__module_name__ = 'hexrat'
__module_version__ = 'v0.9'
__module_description__ = 'SQUEAK!'

import hexchat
import pyperclip
import platform
import datetime
import time
from pygame import mixer
from pathlib import Path

mixer.init()

if platform.system() == "Linux":
     filepath = Path(Path.home(), ".config/hexchat")
elif platform.system() == "Windows": 
     filepath = Path(Path.home(), "AppData/Roaming/HexChat")

#Default values, overruled by config file
logging = True
ratplatforms = "PC-H"
startupgrab = True 
mechacap = 102
quitcap = 51

file = open(Path(filepath, "hexrat.conf"),"r")
config = file.read().splitlines()
file.close
for i in config:
     if i[:17] == "<soundpath_linux>": 
          if platform.system() == "Linux":
               if i.find("$HOME/") > -1:
                    j = i.find("$HOME/")
                    soundpath = Path(Path.home(),i[j+6:])
                    soundpath = str(soundpath) + "/"
               else:
                    soundpath = i[17:]
               soundpath = str(soundpath)
     elif i[:19] == "<soundpath_windows>": 
          if platform.system() == "Windows":
               if i.find("$HOME\\") > -1:
                    j = i.find("$HOME\\")
                    soundpath = Path(Path.home(),i[j+6:])
                    soundpath = str(soundpath) + "\\"
               else:
                    soundpath = i[19:]
               soundpath = str(soundpath)
     elif i[:15] == "<sound_codered>":         
          scr = mixer.Sound(soundpath + i[15:])
     elif i[:16] == "<sound_standard>": 
          sst = mixer.Sound(soundpath + i[16:])
     elif i[:12] == "<sound_skip>":
          ssk = mixer.Sound(soundpath + i[12:])
     elif i[:14] == "<sound_hatsig>":
          stas = mixer.Sound(soundpath + i[14:])
     elif i[:13] == "<sound_alert>": 
          smgs = mixer.Sound(soundpath + i[13:])
     elif i[:12] == "<sound_prep>": 
          sring = mixer.Sound(soundpath + i[12:])
     elif i[:14] == "<sound_squeak>": 
          srat = mixer.Sound(soundpath + i[14:])
     elif i[:13] == "<sound_start>": 
          sbar = mixer.Sound(soundpath + i[13:])
     elif i[:13] == "<sound_cheer>": 
          schr = mixer.Sound(soundpath + i[13:])
     elif i[:9] == "<ratmode>": 
          ratmode = i[9:]
     elif i[:10] == "<copymode>": 
          copymode = i[10:]
     elif i[:11] == "<platforms>": 
          ratplatforms = i[11:]
     elif i[:13] == "<startupgrab>": 
          try:
               startupgrab = bool(i[13:])
          except:
               print("\00304 Problem in hexrat.cfg! <startupgrab> can only be True of False. Defaulting to " + str(startupgrab))
     elif i[:10] == "<mechacap>":
          try:
               mechacap = int(i[10:])
          except:
               print("\00304 Problem in hexrat.cfg! <mechacap> can only be a  number. Defaulting to " + str(mechacap))
     elif i[:9] == "<quitcap>":
          try:
               quitcap = int(i[9:])
          except:
               print("\00304 Problem in hexrat.cfg! <quitcap> can only be a number. Defaulting to " + str(quitcap))
     elif i[:9] == "<logging>":
          try:
               logging =  bool(i[9:])
          except:
               print("\00304 Problem in hexrat.cfg! <quitcap> can only be a number. Defaulting to " + str(quitcap))

alive = "#fuelrats" # target for calls/reports/facts
asafe = hexchat.get_info("nick") # target for safe mode messages

aliastarget = alive
spatcher = "Stuffy"


hexback = False
clients = ["","","","","","","","","","",]
systems = ["","","","","","","","","","",]
plats = ["","","","","","","","","","",]
crits = [False,False,False,False,False,False,False,False,False,False,]

as_casenum = "NO CASE ASSIGNED GO AWAY"
as_client = "NO CASE ASSIGNED GO AWAY"

# Soft-filter list. Nicks listed in this file will have their lines recolored semi-invisible grey. Sad, but some people are just there to be annoying.
try:
     file = open(Path(filepath, "gr1.conf"),"r")
     gr1 = file.read().splitlines()
     file.close 
except: 
     gr1="not this time ratto"

def mode_cb(word, word_eol, userdata): #Hide mode changes in #fuelrats 
     mess = word[1]
     if mess[:13] == "#fuelrats +v " or mess[:13] == "#fuelrats +h ":
          return hexchat.EAT_ALL
     else:
          return hexchat.EAT_NONE
def join_cb(word, word_eol, userdata): #Shorten all Join messages
     global as_client, ratmode, plats
     mess = hexchat.strip(word[2])
     if word[0] in clients:
          for i in range (10):
               if word[0] == clients[i]:
                    your = ""
                    if ratmode == "dispatch":
                         platfix = plats[i] + " "
                    else:
                         platfix = ""
                         
                    if as_client == word[0]:
                         your = "\00304\025\00317Your client\00317\026\00327 "
                    print(your + "\00327"  + platfix + "#" + str(i) + "\00314 " + word[0] + "\00327 joined")
                    return hexchat.EAT_ALL
     else:
          print("\00319" + word[0] + " joined " + mess[mess.find("@"):])
     return hexchat.EAT_ALL
          
def quit_cb(word, word_eol, userdata): #Shorten Quit/leave messages in #fuelrats
     global as_client, ratmode, plats, quitcap
     mess = hexchat.strip(word[2])
     stock = ["FuelRats Web IRC - Provided by KiwiIRC","Connection closed","Going offline, see ya! (www.adiirc.com)","Leaving"]
     reason = ""
     try:
          reason = word[3]
          if reason in stock:
               reason = ""
     except:
          if word[1] not in stock:
               reason = word[1]
     if reason[:6] == "Quit: ":
          reason = reason[6:]
     j = quitcap
     if word[0] in clients:
          for i in range (10): 
               if word[0] == clients[i]:
                    your = ""
                    if ratmode == "dispatch":
                         platfix = plats[i] + " "
                    else:
                         platfix = ""

                    if reason.upper().find("BANNED") > -1: #Ban notifications are given extra space
                         j = 777
                    if as_client == word[0]:
                         your = "\00304\026\00316Your client "
                    print( your + "\00304\026\00316"  + platfix + "#" + str(i) + "\00317\026\00314 " + word[0] + " \00304\026\00316quit\00317\026\00314 " + reason[:j-len(word[0])-len(your)])
                    return hexchat.EAT_ALL
     elif hexchat.get_info("channel") == "#fuelrats":
          print("\00314" + word[0] + " quit " + reason[:j-len(word[0])])
          return hexchat.EAT_ALL
     else:
          return hexchat.EAT_NONE
          
def nick_cb(word, word_eol, userdata): # Nick change, tracked in case clients changes name
     global clients, as_client, spatcher
     for i in range (10):
          if clients[i] == word[0]:
               your=""
               if as_client == word[0]:
                         your = "\00304\026\00316Your client\00317\026\00312 "
               
               print( your + "\00317\026\00312#" + str(i) + " " + word[0] + "\00325 is now known as\00312 #" + str(i) + " "  + word[1])   
               clients[i] = word[1]
               return hexchat.EAT_ALL
     if as_client == word[0]:
          print("\00304>>HEXRAT<< thinks that's your client!")
          as_client = word[1]
     
     if word[0].upper().find("SPATCH") > -1 and word[1].upper().find("SPATCH") == -1 and hexchat.get_info("channel") == "#ratchat":
          print("\00308\026\00317" + word[0] + " \00317\026\00325 reverts back to \00308"+ word[1])
          spatcher = "Stuffy"
          return hexchat.EAT_ALL
     elif word[0].upper().find("SPATCH") == -1 and word[1].upper().find("SPATCH") > -1 and hexchat.get_info("channel") == "#ratchat":
          spatcher = word[1]
          print("\00308" + word[0] + " \00325puts on THE HAT and becomes \00324\026\00317" + spatcher)
          return hexchat.EAT_ALL
     
     return hexchat.EAT_NONE

def chatwatch_cb(word, word_eol, userdata):
     global soundpath, clients, systems, ratmode, as_casenum, as_client, spatcher, gr1, copymode, ratplatforms, plats, crits, mechacap
     nick = hexchat.strip(word[0])
     mess = hexchat.strip(word[1])
     MESS = mess.upper()
     diff = ""
     
     try:
          modechar = word[2]
     except:
          modechar=""

     if hexchat.get_info("channel") == alive and ((mess[:1] == "!" and MESS[:4] != "!KGB") or (mess[:1] == "!" and MESS[:4] != "!OLDKGB") or MESS.find("WELCOME TO") > -1):
          if spatcher != nick:
               hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< identified a Dispatcher: \00324\026\00317' + nick)
          spatcher = nick
     if hexchat.get_info("channel") == "#ratchat" and nick == spatcher and MESS.find("JUST PREP") > -1:
          spatcher = "Stuffy"
          hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< thinks the Dispatcher is actually not.')
     
     if MESS[:9]=='RATSIGNAL' or MESS[:11]=='DRILLSIGNAL':

          if mess.find("#") == 15: # This looks like a legit ratsignal
           
               if mess.find("(Code Red)") > -1:
                    cr = True
               else:
                    cr = False
               
               if mess.find("(ODY_SIGNAL)") > -1:
                    caseplatform = "PC-O"
               elif mess.find("(HOR_SIGNAL)") > -1:
                    caseplatform = "PC-H"
               elif mess.find("(LEG_SIGNAL)") > -1:
                    caseplatform = "PC-L"
               elif mess.find("(PS_SIGNAL)") > -1:
                    caseplatform = "PS"
               elif mess.find("(XB_SIGNAL)") > -1:
                    caseplatform = "XB"
               else:
                    caseplatform = ""
               
               casenum = int(mess[16:18].strip())
               plats[casenum] = caseplatform

               i = mess.find(" – System: ") +12
               j = mess[i:].find("\"")
               systems[casenum] = mess[i:i+j]

               i = mess.find(" – CMDR ") + 8
               j = mess[i:].find("–") -1
               k = mess[i:].find("(") -1
               
               if j > k and k > -1:
                    j = k
               clients[casenum] = mess[i:i+j]
               
               if clients[casenum].find("(In game, location hidden)") > -1:
                    clients[casenum] = clients[casenum][:len(clients[casenum])-27]
               
               if mess.find(") – Nick: ") > -1:
                    i = mess.find(") – Nick: ") + 10
                    j = mess[i:].find("(") -1
                    clients[casenum] = mess[i:i+j]
                    diff = "\00316 Nick!=CMDR"
   
               casclip = "#" + str(casenum) + ":" + clients[casenum] + ":" + systems[casenum]

               if mess.find('" (Unconfirmed ') > -1 or mess.find('Invalid system name') > -1 or mess.find("Permit Required") > -1:
                    print("\00304\026\00316Probably unroutable system!")
                    casclip = casclip + "."
               # This whole "distance thing needs a rework"
               sysrefcheck = ["","Sol","Maia","Rodentia","Fuelum","Rohini"]
               sysref = ""
               if mess.find(" LY from ") > -1:
                    i = mess.find(" LY from ") + 9
                    j = mess[i:].find(")")
                    sysref = mess[i:i+j]
               
               distb = 9999 # Fix this ugly failsafe at some point
               if sysref not in sysrefcheck:
                    if ratmode != "silent":
                         smgs.play()
                    print("\00304 Unlisted reference point! \00315"+ sysref)
               else:
                    if sysref == "Sol":
                         distb = 174
                    elif sysref == "Fuelum":
                         distb = 161
                    elif sysref == "Maia":
                         distb = 383
                    elif sysref == "Rodentia":
                         distb = 22112
                    elif sysref == "Rohini":
                         distb = 7600

               distance = "999"
                      
               if mess.find(" LY from ") > -1:
                    i = mess.find(" LY from ")
                    distance = mess[i-7:i]
                    d2 = distance ######################################################################################################################################
                    if distance.find(" ") > -1:
                         distance = distance[distance.find(" ")+1:]
                    d3 = distance ######################################################################################################################################
                    if distance[-2:-1] == ".":
                         distance = distance[:-2]
                    d4 = distance ######################################################################################################################################
                    d5 = distb #########################################################################################################################################
                    print("\00301System: " + sysref + " | " + str(d2) + " | " + str(d3) + " | Dist " + str(d4) +" | RefDist " + str(d5)) ###################################
                    try:
                         totaldist = int(distance) + distb
                         #totaldist = (int(distance) + distb)*0.8 ###########################################################################################
                         if totaldist <=300:
                              print("\00315Rough distance: Short (less than " + str(totaldist) + " LY from Jackson's)")
                         elif totaldist <=1000:
                              print("\00315Rough distance: Med (less than " + str(totaldist) + " LY from Jackson's)")
                         elif totaldist > 1000:
                              print("\00315Rough distance: LRR (~ " + str(totaldist) + " LY from Jackson's)")
                         if totaldist > 5000:
                              casclip = casclip + "."
                    except:
                         if ratmode != "silent":
                              smgs.play()
                         print("\00304Error calculating distance!!")
               else:
                    casclip = casclip + "."
                    
                    
               if ratmode == "silent":
                    print("\00304\026\00316Ratmode is set to SILENT")               
               print("\00315Casclip:" + casclip)

               if platform.system()=="Windows":
                    try:
                         if copymode == "va":
                              pyperclip.copy(casclip)
                         elif copymode == "system":
                              pyperclip.copy(systems[casenum])
                    except:
                         print("\00316>>HEXRAT<< can't access clipboard!")
               
               if ratmode == "silent":
                    pass
               elif ratmode == "rat":
                    if caseplatform == "PC-O" or caseplatform == "PC-H" or caseplatform == "PC-L" or caseplatform == "PS" or caseplatform == "XB": 
                         if ratplatforms.find(caseplatform) > -1:
                              if cr == True :
                                   scr.play()
                              else:
                                   sst.play()
                         else:
                              ssk.play()
                    else:
                         smgs.play()
                         print("\00304>>HEXRAT<< couldn't sort the ratsignal's platform!")                
               elif ratmode == "dispatch":
                    if cr == True :
                         scr.play()
                    else:
                         sst.play()
               
          else: # Case number not found. Manual ratsignal?
               print("\00320" + modechar + nick + ": " + mess)
               return hexchat.EAT_ALL
               smgs.play()

     # Message was not a Ratsignal
     
     elif (nick == "MechaSqueak[BOT]" or nick == "DrillSqueak[BOT]") and (mess[:26] == 'Successfully closed case #' or mess[:25] == 'Successfully added case #'): # case closed
          try:
               i = int(mess[mess.find("case #")+6:mess.find("case #")+8].strip())
          except:
               print("\00304\026HEXRAT ERROR - failed to get number of closed case")
               smgs.play()
               
          if as_casenum == str(i):
               clear_cb("","","")
          try:
               print("\00321" + nick + " cleared #" + str(i) + " " + clients[i])
          except:
               print("\00304\026HEXRAT ERROR - something with closing the case")
               smgs.play()
               print("\00321" + nick + ": " + mess)
               
          clients[i] = ""
          systems[i] = ""
          plats[i] = ""
          crits[i] = False
          
          if clients[0] + clients[1] +clients[2] +clients[3] +clients[4] +clients[5] +clients[6] +clients[7] +clients[8] +clients[9] == "" and spatcher[-7:].upper() != "SPATCH]":
               hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< cleared all cases. Dispatcher vaporized.')
               spatcher = "Stuffy"
          return hexchat.EAT_ALL

     elif mess[:25] == 'Caution: Client of case #': # client left
          return hexchat.EAT_ALL

     elif mess[-15:] == ') has rejoined!': # client rejoined
          return hexchat.EAT_ALL  
        
     elif (nick == "MechaSqueak[BOT]" or nick == "DrillSqueak[BOT]") and hexchat.get_info("channel") == "#fuelrats" and mess[:9] != "CAUTION: ":# make (probably) unimportant lines shorter and less visible
          if mess[:9] == "CAUTION: ":
               return hexchat.EAT_NONE
          elif len(mess)>mechacap:
               print("\00321" + nick + ": " + mess[:mechacap-3] + "...")
               if logging==True:
                    logfile=open("D:\hexratlog.txt","a")
                    try:
                         logfile.write(str(datetime.datetime.now()) + " <TRIM EVENT> " + mess +" \n")
                    except:
                         logfile.write(str(datetime.datetime.now()) + " <TRIM EVENT> ERROR! \n")     
                    logfile.close()
          else:
               print("\00321" + nick + ": " + mess)      
          return hexchat.EAT_ALL
          
     elif nick == "RatMama[BOT]" and mess[:16] == 'Incoming Client:':
          print("\00321" + nick + ": " + mess)
          return hexchat.EAT_ALL       

     elif mess[:1]=='#' and len(mess) < 8 and MESS[-1:] == "J": #highlight jump calls
          print("\00308" + modechar + nick + ": \00325" + mess)
          
          if nick == spatcher:
               spatcher = "Stuffy"
               hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< thinks the Dispatcher is actually not.')
          if ratmode != "silent":
               srat.play()
          return hexchat.EAT_ALL
          
     elif mess[:5]=='!prep' : #Starting Gun for prep
          if ratmode != "silent":
               sring.play()
          print("\00327" + modechar + nick + "\00327: " + mess)
          return hexchat.EAT_ALL

     elif mess[:1]=='#' and (MESS.find("STDN") > -1 or MESS.find("STNDN")> -1): #highlight standdowns
          print("\00308" + modechar + nick + ": \00320" + mess)
          if ratmode != "silent":
               srat.play()
          return hexchat.EAT_ALL

     elif (nick == as_client): #Highlight the tracked client
          if ratmode == "dispatch":
               platfix = plats[int(as_casenum)] + " "
          else:
               platfix = ""
          if userdata=="action":
               print(" * \00303\026"  + platfix + "#" + as_casenum + " " + nick + "\00317\026\00303 " + mess)
          else:      
               print("\00303\026"  + platfix + "#" + as_casenum + " " + nick + ":\00317\026\00303 " + mess)
          return hexchat.EAT_ALL
          
     elif nick in clients: # tag non-tracked clients with case number
          for i in range (10):
               if nick == clients[i]:
                    if ratmode == "dispatch":
                         platfix = plats[i] + " "
                    else:
                         platfix = ""
                    if userdata=="action":
                         print(" * \00312"  + platfix + "#" + str(i) + " \00312" + nick + "\00307 " + mess)
                    else:
                         print("\00312"  + platfix + "#" + str(i) + " \00312" + nick + ":\00323 " + mess)
          return hexchat.EAT_ALL
                     
     elif MESS.find("HATSIGNAL") > -1: #Hat rats gotta look out for each other
          if ratmode != "silent":
               stas.play()
        
     elif nick == "RatMama[BOT]" and mess[:30] == "[Paperwork] Paperwork for case": #honestly, who wants to see paperwork?
          print("\00321" + nick + ": " + mess)
          return hexchat.EAT_ALL
     
     elif nick == spatcher: #Shiny hat is shiny
          a = ""
          if mess.find(hexchat.get_info("nick")) > -1:
               a = "\00317\026\00329 "
          else:
               a = " "
     
          if userdata=="action":
               print(" * \00324\026\00317" + modechar + nick + "\00317\026\00307" + a + mess)
          else:
               print("\00308\026\00317" + modechar + nick + "\00317\026\00323:" + a + mess)
          return hexchat.EAT_ALL

     elif mess[:1]=='#': #highlight all other reports
          print("\00308" + modechar + nick + ": \00322" + mess)
          return hexchat.EAT_ALL

     elif hexchat.get_info("channel") == alive and MESS.find("IN OPEN") > -1: # highlight IN OPEN
          print("\00308" + modechar + nick + ": \00323" + mess[:MESS.find("IN OPEN")] + "\00304\026\00316" + mess[MESS.find("IN OPEN"):MESS.find("IN OPEN")+7] + "\00317\026\00323" + mess[MESS.find("IN OPEN")+7:])
          return hexchat.EAT_ALL
   
     elif nick in gr1 and hexchat.get_info("channel") == "#ratchat": # example custom color rule. All lines on ratchat
          if userdata=="action":
               print("\00314 * " + modechar + nick + " " + mess)
          else:
               print("\00314" + modechar + nick + ": " + mess)
          return hexchat.EAT_ALL
          
     return hexchat.EAT_NONE

def private_cb(word, word_eol, userdata): # Display all private messages in the #ratchat window
     global clients, plats, crits
     nick = hexchat.strip(word[0])
     mess = hexchat.strip(word[1])
     protobatch = ("","","","","","","","","","")

     if nick == "MechaSqueak[BOT]" and mess.find(" found: #") > -1: # Load the output of !list into HexRat's board
          mess = mess[mess.find(" found: #")+8:]
          i = 0
          r = True
          while i <= 9 and r == True:
               i = i + 1
               #print("case " + mess[1:2] + " " + mess[4:mess.find("(")-1]+ " " + mess[mess.find("(")+1:mess.find(")")]) # Old, fancy formatting for Board
               clients[int(mess[1:2])] = mess[4:mess.find("(")-1].replace(" ", "_")
               plf = mess[mess.find("(")+1:mess.find(")")]
               if plf.find(" CR") > -1:
                    plf = plf[:plf.find(" CR")]
                    crits[int(mess[1:2])] = True
               if plf == "PC HOR":
                    plf = "PC-H"
               elif plf == "PC ODY":
                    plf = "PC-O"
               elif plf == "PC LEG":
                    plf = "PC-L"
               elif plf == "Xbox":
                    plf = "XB"
               elif plf == "Playstation":
                    plf = "PS"
               else:
                    print("\00304Unrecognized platform: " + plf)
                    plf= ""
               plats[int(mess[1:2])] = plf

               if mess.find("), ") > -1:
                    mess = mess[mess.find("), ")+3:]
               else:
                    r = False
          hexchat.command("board show")
     else:
          hexchat.find_context(channel="#ratchat").prnt("\00304   " + word[0] + " whispers: " + word[1])

     return hexchat.EAT_NONE
          
def pull_cb(word, word_eol, userdata):
     global clients, systems, as_client, as_casenum, hexback, copymode
     hexback = False
     try: 
          if int(word[1]) in range(10) and clients[int(word[1])]!="" and systems[int(word[1])] !="":
               as_client=clients[int(word[1])]
               as_casenum=word[1]
               casclip = "#" + as_casenum + ":" + clients[int(as_casenum)] + ":" + systems[int(as_casenum)]
               if platform.system()=="Windows":
                    if copymode == "va":
                         pyperclip.copy(casclip)
                         hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< prepares " + casclip)
                         hexback = True
                         return
                    elif copymode == "system":
                         pyperclip.copy(systems[int(as_casenum)])
                         hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< copies system for " + casclip)                       
          elif int(word[1]) in range(10) and clients[int(word[1])]=="" :
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< can't pull #" + word[1] + " - no name")              
          elif int(word[1]) in range(10) and systems[int(word[1])] !="":
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< can't pull #" + word[1] + " - unknown system ") 
          else:
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< somethingsomething")
     except:
          hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< says no. Try /pull <number")        
     
def focus_cb(word, word_eol, userdata):
     # Scan clipboard for flagged text. If a listed prefix is detected, the message/command is sent to IRC
     global aliastarget, hexback, logging
     i = ["","",""]
     hexback = False
     
     """
     if logging==True:
          logfile=open("D:\hexratlog.txt","a")
          try:
               logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Clipboard: {" + pyperclip.paste().replace('\n', ' <LINE_BREAK> ') + "}\n")
          except:
               logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> <Clipboard logging error> \n")
               #hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< encountered an \00320\026 error \00316writing to the log file!")     
          logfile.close()
     """
     if platform.system()=="Linux":
          return
     if pyperclip.paste()[:4] == '.rc ' :
          hexchat.command("msg #ratchat " + pyperclip.paste()[4:])
          pyperclip.copy('MESSAGE_SENT')
          if logging==True:
               logfile=open("D:\hexratlog.txt","a")
               logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Message sent to #ratchat \n")
               logfile.close()  
     elif pyperclip.paste()[:4] == '.fr ' :
          hexchat.command("msg "+ aliastarget + " " + pyperclip.paste()[4:])
          pyperclip.copy('MESSAGE_SENT')
          if logging==True:          
               logfile=open("D:\hexratlog.txt","a")
               logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Message sent to #fuelrats (if Armed) \n")
               logfile.close()  
     elif pyperclip.paste()[:4] == '.arm':
          arm_cb("","","")          
     elif pyperclip.paste()[:5] == '.safe' :
          safe_cb("","","")           
     elif pyperclip.paste()[:4] == '.ca ' :
          i[1] = pyperclip.paste()[4:6].strip()
          if len(pyperclip.paste()[6:].strip()) > 1:
               i[2]=pyperclip.paste()[6:].strip()
          else:
               i[2] = "-"
          track_cb(i,"","")
          if hexback == True:
               pyperclip.copy('MESSAGE_SENT')
               if logging==True:
                    logfile=open("D:\hexratlog.txt","a")
                    logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Case assigned succesfully \n")
                    logfile.close()  
          else:
               pyperclip.copy('HEXRAT SAYS NO')
               if logging==True:
                    logfile=open("D:\hexratlog.txt","a")
                    logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Case could not be assigned \n")
                    logfile.close()  
     elif pyperclip.paste()[:6] == '.pull ' :
          i[1] = pyperclip.paste()[6:].strip()
          pull_cb(i,"","")
          if hexback == False:
               pyperclip.copy('HEXRAT SAYS NO')
               if logging==True:
                    logfile=open("D:\hexratlog.txt","a")
                    logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Case .pull failed \n")
                    logfile.close()
          else:
               pyperclip.copy('HEXRAT SAYS NO')
               if logging==True:
                    logfile=open("D:\hexratlog.txt","a")
                    logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Case .pull was (probably?) successful \n")
                    logfile.close()
     elif pyperclip.paste()[:6] == '.board' :
          board_cb("","","")
          pyperclip.copy('MESSAGE_SENT')
          pyperclip.copy('HEXRAT SAYS NO')
          if logging==True:
               logfile=open("D:\hexratlog.txt","a")
               logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Displaying the Board \n")
               logfile.close()          
     elif pyperclip.paste()[:3] == '.cc' or pyperclip.paste()[:6] == 'clear.' :
          clear_cb("","","")
          pyperclip.copy('MESSAGE_SENT')
          if logging==True:
               logfile=open("D:\hexratlog.txt","a")
               logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Assigned case cleared \n")
               logfile.close()          
     else:
          pass
          #if logging==True:
          #     logfile=open("D:\hexratlog.txt","a")
          #     logfile.write(str(datetime.datetime.now()) + " <FOCUS EVENT> Clipboard did not contain recognized prefix. Skipping \n")
          #     logfile.close()     



 #   TO DO:  malware payload that spams Aisling Duval propaganda



def track_cb(word, word_eol, userdata): # Set manual tracking on case number and client  
     global as_casenum, as_client, clients, hexback
     hexback = False
     
     try:
          if word[2] == "-":
               as_client = word[9]
          as_casenum = word[1]     
          as_client = word[2]
          hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< is now tracking #" + as_casenum + " " + as_client  )
          hexback = True
     except:
          try:
               if clients[int(word[1])] == "":
                    hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< has no record of client #" + word[1] + ".")
               else:
                    as_casenum = word[1]
                    as_client = clients[int(word[1])]
                    hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< is now tracking #" + as_casenum + " " + as_client  )
                    hexback = True
          except:
               hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< says no.    Try /track <Number> <Nick optional>')       
     return hexchat.EAT_ALL

def spatcher_cb(word, word_eol, userdata):
     global spatcher
     
     try:
          if word[1] == "show":
               hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< thinks the current dispatcher is: \00324\026\00317' + spatcher)       
          elif  word[1] == "set":
               hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< sets \00308\026\00317' + word[2] + '\00317\026\00316 as Dispatcher')
               spatcher = word[2]
          elif word[1] == "clear":
               hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< clears the Dispatcher')
               spatcher = "Stuffy"
          elif word[1] == "":
               pass
          else:
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< can't understand" + word_eol[0])
     except:
          print("\00304\00326HEXRAT ERROR")
           
def clear_cb(word, word_eol, userdata):
     global as_casenum, as_client
     as_casenum = "NO CASE ASSIGNED GO AWAY"
     as_client = "NO CASE ASSIGNED GO AWAY"
     if platform.system()=="Windows":
                    pyperclip.copy(" ")
     hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< cleared your tracked case")
     return hexchat.EAT_ALL

def board_cb(word, word_eol, userdata):
     global clients, systems, as_casenum, as_client, plats, crits
     try:
        a = word[1]
     except:
        print("Error! /board must be given a parameter: show, set or clear")
        return hexchat.EAT_NONE  

     if word[1] == "show":
          j = 0
          for i in range (10):
               if len(clients[i]) > 0:
                    j = len(clients[i])       
          if j > 0 :
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< is aware of the following cases:")
               for i in range (10):
                    if crits[i] == True:
                         color = "\00304"
                    else:
                         color = "\00316"
                    
                    if clients[i] == as_client: 
                         try:
                              hexchat.find_context(channel="#ratchat").prnt(color + "\026" + plats[i] + "   #" + str(i) + ":" + clients[i] + ":" + systems[i] )
                         except:
                              hexchat.find_context(channel="#ratchat").prnt(color + "\026" + plats[i] + "   #" + str(i) + ":" + clients[i])
                    elif clients[i] != "":
                         try:
                              hexchat.find_context(channel="#ratchat").prnt(color + plats[i] + "   #" + str(i) + ":" + clients[i] + ":" + systems[i] )
                         except:
                              hexchat.find_context(channel="#ratchat").prnt(color + plats[i] + "   #" + str(i) + ":" + clients[i])
          elif as_casenum != "NO CASE ASSIGNED GO AWAY":
               print("branch 2")
               try:
                    hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< is manually tracking\00316\026 #" + as_casenum + " " + as_client + " ")
               except:
                    try:
                         hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< manually tracking\00316\026 #" + as_casenum + " ")
                    except:
                         hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< Failed executing /board")
          else:
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< Nothing on the board")
     elif word[1] == "set":
          try:
               systems[int(word[2])] = word_eol[4]
          except:
               pass
          try:
               clients[int(word[2])] = word[3]
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< sets client " + word[2] + " as "+word[3])
          except:
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< says no. Try /board_set <number> <clientname>")      
          return hexchat.EAT_ALL
          
     elif word[1] == "setplat":
          try:
               lop = ("PC","PC-O","PS","XB")
               if clients[int(word[2])] != "" and word[3] in lop:
                    plats[int(word[2])] = word[3]
                    hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< sets client " + word[2] + "'s platform to " + word[3])
               else:
                    hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< says no to " + word_eol[0] + ". Try /board setplat number platform") 
          except:
               hexchat.find_context(channel="#ratchat").prnt("\00304>>HEXRAT<< says no to " + word_eol[0] + ". Try /board setplat number platform")
               return hexchat.EAT_ALL
     elif word[1] == "clear":
          try:
               if word[2] == "all":
                    hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< starts to wipe the board")
                    for i in range(10):
                         if clients[i] != "":
                              hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< cleared #" + str(i))
                              clients[i] = ""
                              systems[i] = ""
                              plats[i] = ""
                              crits[i] = False
               else:
                         hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< cleared #"+word[1])
                         clients[int(word[2])] = ""
                         systems[int(word[2])] = ""
                         plats[int(word[2])] = ""
                         crits[int(word[2])] = False
          except:
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< couldn't clear the board")      
          return hexchat.EAT_ALL
     else:
          hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< can't understand" + word_eol[0] + " . Valid parameters are show, set, setplat and clear")
          pass
     
def safe_cb(word, word_eol, userdata):
     global aliastarget, asafe
     aliastarget = asafe 
     hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< is sending fr to "+aliastarget)
     if platform.system()=="Windows":
          pyperclip.copy('MESSAGE_SENT')
     if logging==True:
          logfile=open("D:\hexratlog.txt","a")
          logfile.write(str(datetime.datetime.now()) + ' <FOCUS EVENT> Fuelrats sensmode is now "SAFE" \n')
          logfile.close() 
def arm_cb(word, word_eol, userdata):
     global aliastarget, alive
     aliastarget = alive
     hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< is sending fr to \00320\026"+ aliastarget)     
     if platform.system()=="Windows":
          pyperclip.copy('MESSAGE_SENT')
     if logging==True:
          logfile=open("D:\hexratlog.txt","a")
          logfile.write(str(datetime.datetime.now()) + ' <FOCUS EVENT> #fuelrats sendmode is now "ARMED" + \n')
          logfile.close()  

def ratmode_cb(word, word_eol, userdata):
     global ratmode
     try:
          if word[1]=="silent" or word[1]=="off":
               ratmode="silent"
          elif word[1]=="" or word[1]=="rat":
               ratmode="rat"
          elif word[1]=="hat" or word[1]=="spatch" or word[1]=="dispatch":
               ratmode="dispatch"
          else:
               hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< says no, "' + word[1] + '" is not a valid Ratmod. Try rat, dispatch or silent')
          hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< Ratmode is: " + ratmode  )     
     except:
          hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< accepts only: "rat", "hat", "silent"')        
     return hexchat.EAT_NONE
     
def hat_cb(word, word_eol, userdata):
     global aliastarget, alive, asafe, ratmode, spatcher
     if hexchat.get_info("nick").upper().find("SPATCH") > -1:
            if hexchat.get_info("nick").upper()[-10:] == "[DISPATCH]":
                if aliastarget == alive:
                    hexchat.command("nick " + hexchat.get_info("nick")[:-10])
                    spatcher == "Stuffy"
                else:
                    print("\00316 * You pretend to revert back to \00316" + hexchat.get_info("nick")[:-10])
            else:
                hexchat.find_context(channel="#ratchat").prnt('\00316>>HEXRAT<< heard you, but was confused by your tag(s). \00304Remove your hat yourself.')
     else:
          if aliastarget == alive:
               hexchat.command("nick " + hexchat.get_info("nick") + "[Dispatch]")
               ratmode = "dispatch"
               spatcher == hexchat.get_info("nick")
          else:
               print("\00329 * You make sure no one sees you, then pretend to put on \00320THE HAT\00329 to become \00320" + hexchat.get_info("nick") + "[Dispatch]")
     return hexchat.EAT_ALL	
     
def open_cb(word, word_eol, userdata):
     global startupgrab
     if hexchat.get_info("channel") == "#ratchat":
          hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< watches your every move. Type /hexhelp if this scares you")
          if startupgrab == True:
               hexchat.command("msg MechaSqueak[BOT] !list")
def justprep_cb(word,word_eol,userdata):
     global clients, aliastarget, asafe
     case = 999
     
     try:
          if word[1][:1]=="#":
               case = int(word[1][1:])
          else:
               case = int(word[1])
               
          if clients[case] != "" and int(word[2][0]) < 10 and (word[2][1] =="j" or word[2][2] =="j"):
               hexchat.command("msg " + aliastarget + " !prep-auto " + str(case))   
               if aliastarget == alive:
                    hexchat.command("msg #ratchat Just prepping")
               else:
                    print("\00316You pretend to inform the rats you are just prepping")
               time.sleep(1)
               hexchat.command("msg " + aliastarget + " #" + str(case) + " " + word[2])
          elif clients[case] == "":
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< knows of no such client")
          else: 
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< is not sure what went wrong, but something did")
               print(word[0]," ", word[1]," ", word[2])
               print(clients[case])
               print(word[2][0])
               print(word[2][1])
               print(word[2][2])
     except:
          hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< says no")
     return hexchat.EAT_NONE      
 
def welcome_cb(word, word_eol, userdata):
     global aliastarget, spatcher

     # Target case numbers instead of names

     try:
          if spatcher == "Stuffy" or spatcher == hexchat.get_info("nick") :

               #if hexchat.get_info("nick")[-10:] != "[Dispatch]":
               #     hat_cb("","","")
               if word[1] in clients:
                    hexchat.command("msg " + aliastarget + " " + word[1] +  ' we have received your distress call, welcome to the Fuel Rats. Please let us know once your non-essential modules are powered down.')
                    hexchat.command("msg " + aliastarget + ' If at any time during the rescue an "Oxygen depleted" countdown appears on your screen, tell us immediately.')
               else:
                    hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< /we " + word[1] +"    \00304failed\00316: That's not a client")
          else:
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< flinched during /we : \00308" + spatcher + "\00316 already appears to be a dispatcher")
     except:
          hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< /we \00304failed\00316 : No client set")
     return hexchat.EAT_ALL

def th_cb(word, word_eol, userdata):
     global aliastarget
     try:
          if word[1] in clients:
               hexchat.command("msg " + aliastarget + " " + word[1] +  ': Your ship is now receiving fuel, thank you for calling the Fuel Rats! Please return to the game and talk to your rats on wing/team comms about some quick fuel tips.')
          else:
               hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< /th " + word[1] +"    \00304failed\00316: That's not a client")
     except:
          hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< /th \00304failed\00316 : No client set")
     return hexchat.EAT_ALL
     
def hexhelp_cb(word, word_eol, userdata):
     hexchat.find_context(channel="#ratchat").prnt("\00316>>HEXRAT<< can perform the following commands:  ")
     hexchat.find_context(channel="#ratchat").prnt("\00316 /hat  (automatically switches between on and off)")
     hexchat.find_context(channel="#ratchat").prnt("\00316 /ratmode <rat|silent|dispatch>")
     hexchat.find_context(channel="#ratchat").prnt("\00316 /track <existing case number>  OR  <number> <nick>")
     hexchat.find_context(channel="#ratchat").prnt("\00316 /clear (clear tracked case/nick)")
     hexchat.find_context(channel="#ratchat").prnt("\00316 /board   (list currently active cases)")
     hexchat.find_context(channel="#ratchat").prnt("\00316 /board set <number> <nick> <system>")
     hexchat.find_context(channel="#ratchat").prnt('\00316 /board clear <case>  OR "all"')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /board setplat <case> <platform>')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /pull <case>  sends case to clipboard')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /safe   for testing')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /arm     return to live mode')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /jp <case> <jumps>     \00304FORBIDDEN BARRAGE!\00316 Use powers responsibly.')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /we <nick>" Displays "Welcome" to #fuelrats" and puts on THE HAT')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /th <nick>" Displays "Thx/bye" to #fuelrats"')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /hr    If hexrat-loader is running, launch/reload hexrat')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /spatch show    Show the currently tracked dispatcer')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /spatch set    Manually set a dispatcher. (Might be automatically overwritten')
     hexchat.find_context(channel="#ratchat").prnt('\00316 /spatch clear    Unsets current dispatcher')
     hexchat.find_context(channel="#ratchat").prnt("")

hexchat.hook_print("Private Message", private_cb)
hexchat.hook_print("Private Message to Dialog", private_cb)
hexchat.hook_print("Private Action", private_cb)
hexchat.hook_print("Private Action to Dialog", private_cb)

hexchat.hook_print("Channel Message", chatwatch_cb, userdata="message")
hexchat.hook_print("Channel Msg Hilight", chatwatch_cb, userdata="action")
hexchat.hook_print("Channel Action", chatwatch_cb, userdata="message")
hexchat.hook_print("Channel Action Hilight", chatwatch_cb, userdata="action")

hexchat.hook_print("Raw Modes", mode_cb)
hexchat.hook_print("Join", join_cb)
hexchat.hook_print("Part", quit_cb)
hexchat.hook_print("Part with Reason", quit_cb)
hexchat.hook_print("Quit", quit_cb)
hexchat.hook_print("Change Nick", nick_cb)

hexchat.hook_command("hexvar", board_cb)
hexchat.hook_command("hat", hat_cb)
hexchat.hook_command("ratmode", ratmode_cb)
hexchat.hook_command("ca", track_cb)
hexchat.hook_command("track", track_cb)
hexchat.hook_command("clear", clear_cb)
hexchat.hook_command("cc", clear_cb)
hexchat.hook_command("we", welcome_cb)
hexchat.hook_command("th", th_cb)
hexchat.hook_command("hexhelp", hexhelp_cb)
hexchat.hook_command("board", board_cb)
hexchat.hook_command("pull", pull_cb)
hexchat.hook_command("justprep", justprep_cb)
hexchat.hook_command("jp", justprep_cb)
hexchat.hook_command("safe", safe_cb)
hexchat.hook_command("arm", arm_cb)
hexchat.hook_command("spatcher", spatcher_cb)
hexchat.hook_command("spatch", spatcher_cb)

hexchat.hook_print("Focus Window", focus_cb)
hexchat.hook_print("Open Context", open_cb)

print("\00316>>HEXRAT<< " + __module_version__ +  " initialized")
sbar.play()
