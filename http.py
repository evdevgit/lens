#from tcp import TCPApplicationLayer
from ethernet import NetLayer
from tornado import gen, httputil

#class HTTPLayer(TCPApplicationLayer):
class HTTPLayer(NetLayer):
    IN_TYPES = {"TCP App"}
    OUT_TYPE = "HTTP"
    STATE_START = "start"
    STATE_HEADERS = "headers"

    def __init__(self, sender, reciever, *args, **kwargs):
        super(HTTPLayer, self).__init__(*args, **kwargs)
        self.cl_state = self.STATE_START
        self.sv_state = self.STATE_START
        self.client = sender
        self.server = reciever

        self.req = self.request()
        self.req.next()

        self.resp = self.response()
        self.resp.next()

    @gen.coroutine
    def on_read(self, src, data, conn):
        if src == self.client:
            # Client -> Server
            self.req.send(data)
        elif src == self.server:
            self.resp.send(data)
        else:
            print "Unknown src: {}; ({} -> {})".format(src, self.client, self.server)
        yield self.bubble(src, data, conn)

    def request(self):
        req_line = yield 
        req = httputil.parse_request_start_line(req_line.strip())
        headers = httputil.HTTPHeaders()
        while True:
            header_line = yield
            if not header_line.strip():
                break
            headers.parse_line(header_line.strip())
        print "REQUEST", req, headers
        body = ""
        while True:
            body += yield

    def response(self):
        start_line = yield 
        resp = httputil.parse_response_start_line(start_line.strip())
        headers = httputil.HTTPHeaders()
        while True:
            header_line = yield
            if not header_line.strip():
                break
            headers.parse_line(header_line.strip())
        print "RESPONSE", resp, headers
        body = ""
        while True:
            body += yield


    @gen.coroutine
    def on_close(self, src, conn):
        yield super(HTTPLayer, self).on_close(src)

