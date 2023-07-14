###############################################################################
# Name: gcode_pushover.py
# Desc: send messages via gcode to pushover
# Note: requests and apprise libraries missing from sonic pad, this prevents 
#       using moonraker notifier, and is why urllib3 is used instead
#       Save to /usr/share/klipper/klippy/extras on sonic pad
#
# Note: bits of code taken directly from Eric Callahan's gcode_shell_command.py
### Imports ###################################################################
import urllib3
from io import BytesIO
import logging

### Class #####################################################################
class PushoverNotifier:
    URL = 'https://api.pushover.net/1/messages.json'
    HELP = 'send messages via gcode to pushover'

    def __init__(self,config):
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')

        self.user_token = config.get('user')
        self.app_token = config.get('token')
        self.attachment = config.get('attach','')
        self.verbose = config.getboolean('verbose', True)

        self.gcode.register_mux_command(
            'SEND_PUSHOVER_MESSAGE','CMD',self.name,
            self.send_message,
            desc=self.HELP
        )
    
    def send_message(self,params):
        '''Send message to pushover'''
        title = params.get('TITLE','Test Message')
        message = params.get('MESSAGE','This is a test')
        priority = params.get('PRIORITY','0')

        try:
            http = urllib3.PoolManager()

            fields = {
                'token':self.app_token,
                'user':self.user_token,
                'priority':priority,
                'title':title,
                'message':message,
            }

            if self.attachment:
                try:
                    pic = BytesIO()
                    request = http.request('GET',self.attachment,preload_content=False)
                    while True:
                        data = request.read(1000)
                        if not data:
                            break
                        pic.write(data)
                    
                    if pic.getbuffer().nbytes > 0:
                        fields['attachment'] = ('snapshot.jpg',pic.getbuffer(),'image/jpeg')
                    request.release_conn()
                except urllib3.exceptions.MaxRetryError:
                    self.gcode.respond_info('Retry Error getting attachment')

            
            response = http.request('POST',self.URL,fields=fields)
            if self.verbose:
                self.gcode.respond_info('Response Status: {}'.format(response.status))
                self.gcode.respond_info('Response: {}'.format(response.data.decode()))

            response.release_conn()
        
        
        except Exception as e:
            #logging.exception('pushover_message: {%s}' % (str(e)))
            raise self.gcode.error("Error sending pushover message {%s}" % (str(e)))


def load_config_prefix(config):
    return PushoverNotifier(config)