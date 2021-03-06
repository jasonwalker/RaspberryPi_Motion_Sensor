import web,sys,time,traceback
import RPi.GPIO as GPIO
from threading import Thread,current_thread
from collections import deque
from Config import DATAPIN

MOVEMENTDATA = deque(maxlen=1440)

def format(t):
    return 'Date.UTC(%i, %i, %i, %i, %i, %i)' % \
      (t.tm_year,t.tm_mon-1,t.tm_mday,t.tm_hour, t.tm_min,t.tm_sec)
    
def startCollectingData():
    data = __DataClass()  
    data.start()  
    
def getDataAndStartTime():
    dataString = ','.join(map(str, MOVEMENTDATA))
    #subtract minutes from current time
    current = time.time() - (60 * len(MOVEMENTDATA)) 
    return dataString, format(time.localtime(current))    
    
class __DataClass(Thread):
    """Takes a list-type object and populates it with data from RPi
    IO port"""
    def __init__(self):
        Thread.__init__(self)
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(DATAPIN, GPIO.IN)
            self.daemon = True
        except Exception, msg:
            print 'exception thrown',msg
            GPIO.cleanup()
        
    def run(self):
        motion = 0
        try:
            seconds = 0
            while 1:
                curTime = time.localtime()
                #if seconds val just flipped from high to low number; a new minute started
                if seconds > curTime.tm_sec:
                    MOVEMENTDATA.append(motion)
                    motion = 0
                motion += GPIO.input(DATAPIN)
                seconds = curTime.tm_sec
                time.sleep(1)
        except:
            print traceback.print_exc()
            print 'cleaning up'
        finally:
            GPIO.cleanup()

