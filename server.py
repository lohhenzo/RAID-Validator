import tornado.ioloop
import tornado.web

import raid

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(raid.main())

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
