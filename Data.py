import web,sys,time,traceback
import RPi.GPIO as GPIO
from threading import Thread,current_thread
from copy import copy
from collections import deque
from Config import DATAPIN

def format(t):
    return 'Date.UTC(%i, %i, %i, %i, %i, %i)' % \
      (t.tm_year,t.tm_mon-1,t.tm_mday,t.tm_hour, t.tm_min,t.tm_sec)
    
class DataClass(Thread):
    def __init__(self):
        Thread.__init__(self)
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(DATAPIN, GPIO.IN)
            self.MOVEMENTDATA = deque(maxlen=1440)
            self.start()
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
                    self.MOVEMENTDATA.append(motion)
                    motion = 0
                motion += GPIO.input(DATAPIN)
                seconds = curTime.tm_sec
                time.sleep(1)
        except:
            print traceback.print_exc()
            print 'cleaning up'
        finally:
            GPIO.cleanup()
           
    def getDataAndStartTime(self):
        d2 = copy(self.MOVEMENTDATA)
        dataString = ','.join(map(str, d2))
        current = time.time() - (60 * len(d2)) #subtract minutes from current time
        return dataString, format(time.localtime(current))
