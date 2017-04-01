from flask import *
import json
app = Flask(__name__) 

SERVE_CONTENT_TYPE = ['html', 'txt', 'pdf', 'js', 'png', 'css', 'jpg', 'mp4']
SERVE_CONTENT_PREFIX = 'example'

def DictHeaders(headers):
    ret = dict()
    for k,v in headers.items():
        ret[k] = v
    return ret

@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory('static/', 'index.html')

@app.route('/<userpath>/<content>')
def stupid_content(userpath, content):
    
    req_hdr = json.dumps( DictHeaders(request.headers) )
    req_cookie = json.dumps( DictHeaders(request.cookies) )
    ret = send_from_directory('static/', content)
    
    # appending response header from query strings
    for k,v in request.args.items():
        if v == '':
            del ret.headers[k]
        else:
            ret.headers[k]=v

    # appending response header from request header "ResHeader" json format
    if 'Set-Response-Header' in request.headers:
        try:
            hdr = json.loads( request.headers['Set-Response-Header'] )
            for k,v in hdr.items():
                if v == '':
                    del ret.headers[k]
                else:
                    ret.headers[k]=v
        except Exception as err:
            pass

    res_hdr = json.dumps( DictHeaders(ret.headers) )
    ret.headers['Request-Headers']=req_hdr
    ret.headers['Response-Headers']=res_hdr
    ret.headers['Request-Cookies']=req_cookie

    return ret


if __name__ == '__main__':
    app.run()
