import tornado.ioloop
import tornado.web

import raid

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('test')

    def post(self):
        po = self.get_argument('po')
        self.write(str(raid.main(po)))

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8890)
    tornado.ioloop.IOLoop.instance().start()
