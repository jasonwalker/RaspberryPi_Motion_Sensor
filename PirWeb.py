#!/usr/bin/python
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.template as template

from tornado.web import RequestHandler
from tornado.escape import utf8

import sys,os, time,traceback,base64,re
from Data import getDataAndStartTime, startCollectingData
from Config import TITLE, SUBTITLE, YAXISTITLE, USERNAME, PASSWORD, PORT, CERTPATH, KEYPATH
import subprocess
from subprocess import Popen, PIPE, STDOUT

def isCameraAvailable():
    try:
        p = Popen("/opt/vc/bin/vcgencmd get_camera", shell=True, stdin=PIPE, stdout=PIPE, stderr=None, close_fds=True)
        cameraStatus = p.stdout.read(60)
        print cameraStatus
        m = re.search('supported=(\d) detected=(\d)', cameraStatus)
        return m and len(m.groups()) == 2 and m.group(1) == '1' and m.group(2) == '1'
    except:
        return False
    
cameraAvailable = isCameraAvailable()

def make_app():
    pages = [('/', MotionHandler)]
    if cameraAvailable:
        pages.extend([('/img.jpg', ImageHandler),
                      ('/current', CurrentHandler)])
    
    return tornado.web.Application(pages, 
        debug=True,
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"))    

class BaseHandler(RequestHandler):

    def authorized(self):
        auth = self.request.headers.get('Authorization', None)
        if auth:
           username,password = base64.decodestring(auth.split()[1]).split(':')
           if username == USERNAME and password == PASSWORD:
              return True

        self.set_header('WWW-Authenticate','Basic realm="Motion Detector"')
        self.set_status(401, "not authorized")
        return False

class MotionHandler(BaseHandler):
    def get(self):
        if not self.authorized():
            return
        data, startTime = getDataAndStartTime()
        v = self.render('index.html', data2=data,start=startTime,title=TITLE, subtitle=SUBTITLE, yaxisTitle=YAXISTITLE,cameraAvailable=cameraAvailable)
        return v

class CurrentHandler(BaseHandler):
    def get(self):
        if not self.authorized():
            return
        self.set_header("Content-Type", "text/html")
        self.write('''\
<!DOCTYPE html>
<html>
<body>
<h2>Current</h2>
<img src="img.jpg" alt="Current View">

</body>
</html> 
''')

class ImageHandler(BaseHandler):
    def get(self):
        if not self.authorized():
           return
        #~ self.set_header("Content-Type", "image/jpeg")
        #~ self.write(testimage)
        self.set_header("Content-Type", "/images/jpeg")
        proc = subprocess.Popen(["raspistill", "-e", "jpg", "-o", "-", "-q","10"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = proc.communicate()
        self.write(out)   

if __name__ == "__main__":
    startCollectingData()
    app = tornado.httpserver.HTTPServer(make_app(),
    # if you want HTTPS, uncomment and put in certificate and keys
    #ssl_options={"certfile":CERTPATH,
    #             "keyfile":KEYPATH}
    )
    app.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
