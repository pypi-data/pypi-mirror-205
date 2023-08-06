# ================================================================
# Log.py - Logging support. Output to .log file and/or terminal.
# ================================================================
import os
import logging

# ================================================================
def test(Message) :
  print('LogTest: ' + Message)


# ================================================================
# LogSetup() - Set up logging - Note that it prints to stdout too.
# Inputs: LogFileNamePrefix - of the form "/somepath/myapp.py"
#
def setup(LogFileNamePrefix) :
  AppFullFileName= LogFileNamePrefix
  # https://docs.python.org/3/library/os.path.html
  AppNameSplitExt= os.path.splitext(AppFullFileName)  # [0]=path/name, [1]= ext
  LogFileName= AppNameSplitExt[0] + '.log'

  logging.basicConfig(filename=LogFileName,
                      encoding='utf-8',
                      level=logging.INFO,
                      filemode='a',
                      # %(msecs)d - msec as int. %(name)s - username as string. %(levelname)s - debug level as string.
                      format='[%(asctime)s %(levelname)s]: %(message)s',
                      #datefmt='%H:%M:%S'
                      # %a - day of week, %d - day of month, %b - month
                      datefmt='%a, %d %b %Y %H:%M:%S'
                      )
  #end setup

# ================================================================
# Output to tty & log file
# Inputs:
#   LogLevel - Error, Warning, Info
def write(LogLevel, Message) :
  print(Message)
  # TBD - print at appropropriate level
  # logging.INFO = 20
  logging.info(Message)

def write(Message) :
  print(Message)
  #print('LogWrite!')
  logging.info(Message)

