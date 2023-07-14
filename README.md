# Sonicpad
Sonic pad scripts, well currently just the one script, the purpose of which is to allow sending pushover notifications from the Creality Sonic Pad. If some time in the future Creality adds apprise or some enterprising individual figures out how to install it, this script is obsolete as moonraker will be able to do everything this can without having to root and appears to have better hooks in to what is going on in the printer. 

### Prerequisites 
First you will need to be able to login via ssh as root into your Sonic Pad. Creality provides an easy way to get the root credentials now from Sonic Pad > Configure > Other Settings > Advanced options > Root Account. You will need to agree to the root notice. Understanding you can mess up your Sonic Pad if you are not careful, **do at your own risk**.

### Installation
If you are choosing to continue, you can either ssh in to your sonic pad with something like putty or use WinSCP to copy the files to your sonic pad, choice is yours. 
#### Putty
1. ssh into your Sonic Pad then `cd /user/share/klipper/klippy/extras`
2. using vi make the file `vi gcode_pushover.py. press` "I" then paste in the text (right click in putty), then press esc, then type ":wq" to save and close the file.
3. restart the Sonic Pad.

### Printer.cfg 
Backup your printer.cfg file just to be safe and add the macros in the example_printer.cfg, making sure to update the user token and app token with your tokens from pushover. if you don’t have a webcam attached to your Sonic pad remove the URL in the attach line. Update any of the SEND_PUSHOVER_MESSAGE lines, making sure the title and message strings are surrounded by double quotes ("")
Save printer.cfg and restart klipper. You should now be able to go to the console and type "PUSH_TEST"

### Light Reading
The original inspiration for this is the gcode_shell_command.py written by Eric Callahan. 
[Original Post the led me down this rabbit hole]( https://www.teamfdm.com/forums/topic/816-howto-pushover-notifications-for-completed-prints-to-your-phone/)

[More information on Eric’s gcode_shell_command.py]( https://github.com/th33xitus/kiauh/blob/master/docs/gcode_shell_command.md)
