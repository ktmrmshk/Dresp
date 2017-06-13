from flask import *
import json
import re
from datetime import datetime
app = Flask(__name__) 

SERVE_CONTENT_TYPE = ['html', 'txt', 'pdf', 'js', 'png', 'css', 'jpg', 'mp4']
SERVE_CONTENT_PREFIX = 'example'

def DictHeaders(headers):
    ret = dict()
    for k,v in headers.items():
        ret[k] = v
    return ret

def makeIntentErrRes(status_code):
    pd = {}
    pd['title'] = 'Intentional {} page'.format(status_code)
    pd['body'] = []
    pd['body'].append('This page generated by intentionally from user request')
    pd['body'].append('date: {}'.format(datetime.now()))
    return render_template('debug.html', pd=pd), status_code



@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory('static/', 'index.html')

def pickup_key(request, key):
    '''
    return None, if request doesn't have the key
    
    * Query string is checked first, following by Request Header "Set-Response-Header".
    '''
    # check query
    if key in request.args:
        return request.args[key]

    # check request header
    if 'Set-Response-Header' in request.headers:
        try:
            hdr = json.loads( request.headers['Set-Response-Header'] )
            if key in hdr:
              return hdr[key]
        except Exception as err:
            pass
    return None
        


@app.route('/<userpath>/<content>')
def stupid_content(userpath, content):

    ### 4xx/5xx response
    prefix = re.search(r'^([45]\d{2})\..+$', content)
    if prefix is not None:
        #status_code=int(prefix.group(1))
        #pd = {}
        #pd['title'] = 'Intentional {} page'.format(status_code)
        #pd['body'] = []
        #pd['body'].append('This page generated by intentionally from user request')
        #pd['body'].append('date: {}'.format(datetime.now()))
        #return render_template('debug.html', pd=pd), status_code
        return makeIntentErrRes( int(prefix.group(1)) )
    
    if 'Set-Status-Code' in request.args.keys():
        query_val = re.search(r'^([45]..)$', request.args['Set-Status-Code'])
        if query_val is not None:
            return makeIntentErrRes( int(query_val.group(1)) )

    if 'Set-Status-Code' in request.headers:
        header_val = re.search(r'^([45]..)$', request.headers['Set-Status-Code'])
        if header_val is not None:
            return makeIntentErrRes( int(header_val.group(1)) )


    ### 301, 302, 303, 305, 307 Redirect
    if 'Set-Status-Code' in request.args.keys():
        query_val = re.search(r'^(30[12357])$', request.args['Set-Status-Code'])
        if query_val is not None:
            status_code = int(query_val.group(1))
            redirect_to=pickup_key(request, 'Location')
            if redirect_to is None:
                redirect_to='https://www.akamai.com/'
            return redirect(redirect_to, status_code)

    if 'Set-Status-Code' in request.headers:
        header_val = re.search(r'^(30[12357])$', request.headers['Set-Status-Code'])
        if header_val is not None:
            status_code = int(header_val.group(1))
            redirect_to=pickup_key(request, 'Location')
            if redirect_to is None:
                redirect_to='https://www.akamai.com/'
            return redirect(redirect_to, status_code)


    ### for another request: other than 3xx redirect nor 4xx/5xx

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
    app.run(debug=True, host='0.0.0.0')
