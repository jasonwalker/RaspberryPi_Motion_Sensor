#!/usr/bin/python
import web,sys,os,time,traceback,base64
from Data import DataClass
from Config import TITLE, SUBTITLE, YAXISTITLE, USERNAME, PASSWORD, PORT
urls = ('/', 'index',
        '/favicon.ico','favicon')
mainDir = os.path.dirname(os.path.realpath(__file__))
render = web.template.render(os.path.join(mainDir, 'templates'))
dataClass = DataClass()
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

class index:
    def GET(self):
        if not authorized():
            return
        data, startTime = dataClass.getDataAndStartTime()
        v = render.index(data,startTime,TITLE, SUBTITLE, YAXISTITLE)
        return v

class MotionApp(web.application):
    def run(self, port=PORT, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))
        
if __name__ == "__main__":
    app = MotionApp(urls, globals())
    app.run()
