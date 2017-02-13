#!/usr/bin/python
import web,sys,os,time,traceback,base64,re
from Data import getDataAndStartTime, startCollectingData
from Config import TITLE, SUBTITLE, YAXISTITLE, USERNAME, PASSWORD, PORT
import subprocess
from subprocess import Popen, PIPE, STDOUT
from web.wsgiserver import CherryPyWSGIServer

#add in if you want HTTPS
#CherryPyWSGIServer.ssl_certificate = "/usr/local/bin/PIR/selfsigned.crt"
#CherryPyWSGIServer.ssl_private_key = "/usr/local/bin/PIR/private.key"

p = Popen("/opt/vc/bin/vcgencmd get_camera", shell=True, stdin=PIPE, stdout=PIPE, stderr=None, close_fds=True)
cameraStatus = p.stdout.read(60)
print cameraStatus
m = re.search('supported=(\d) detected=(\d)', cameraStatus)
cameraAvailable = m and len(m.groups()) == 2 and m.group(1) == '1' and m.group(2) == '1'
    
if cameraAvailable:
    urls = ('/', 'index',
            '/img.jpg', 'img',
            '/current', 'current',
            '/js/(.*)', 'static',
            '/favicon.ico','favicon')
else:
    urls = ('/', 'index',
            '/js/(.*)', 'static',
            '/favicon.ico','favicon')
mainDir = os.path.dirname(os.path.realpath(__file__))
render = web.template.render(os.path.join(mainDir, 'templates'))


with open(os.path.join(mainDir, 'favicon.ico'),'rb') as iconFile:
    icon = iconFile.read()

def authorized():
    credentials = web.ctx.env.get('HTTP_AUTHORIZATION')
    if credentials is not None:
        try:
            username,password = base64.decodestring(credentials.split()[1]).split(':')
            if username==USERNAME and password==PASSWORD:
                return True
        except Exception, msg:
            print "an exception",msg
    web.header('WWW-Authenticate','Basic realm="Motion Detector"')
    web.ctx.status = '401 Unauthorized'
    return False    

class favicon:
    def GET(self):
        if not authorized():
            return
        web.header('Content-Disposition','icon')
        return icon

class current:
    def GET(self):
        if not authorized():
            return
        return '''\
<!DOCTYPE html>
<html>
<body>

<h2>Current</h2>
<img src="img.jpg" alt="Current View">

</body>
</html> 
'''

class img:
    def GET(self):
        if not authorized():
            return
        web.header("Content-Type", "/images/jpeg")
        proc = subprocess.Popen(["raspistill", "-e", "jpg", "-o", "-", "-q","10"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = proc.communicate()
        return out      
        

class index:
    def GET(self):
        if not authorized():
            return
        data, startTime = getDataAndStartTime()
        v = render.index(data,startTime,TITLE, SUBTITLE, YAXISTITLE)
        return v

class static:
    def GET(self, path):
        try:
            with open(os.path.join(mainDir, 'js', path), 'r') as f:
                return f.read()
        except Exception, msg:
            web.ctx.status = '404 Not Found'
            return 

class MotionApp(web.application):
    def run(self, port=PORT, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))
        
if __name__ == "__main__":
    try:
        startCollectingData()
        app = MotionApp(urls, globals())
        app.run()
    except:
        with open('problem.txt','w') as f:
            traceback.print_exc(file=f)
