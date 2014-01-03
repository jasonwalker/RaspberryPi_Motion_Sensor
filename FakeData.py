import time,random

def format(t):
   return 'Date.UTC(%i, %i, %i, %i, %i, %i)' % (t.tm_year,t.tm_mon-1,t.tm_mday,t.tm_hour, t.tm_min,t.tm_sec)

class DataClass:

    def getDataAndStartTime(self):
        cur = time.localtime()
        i = time.mktime(cur)
        data = [random.randint(0,60) for v in range(0,1000)]
        startTime = time.time() - (60 * len(data))
        return ','.join(map(str, data)), format(time.localtime(startTime))

      
