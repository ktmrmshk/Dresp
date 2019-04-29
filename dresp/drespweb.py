from flask import *
import json, os, re, random
from imgen import imgen, imgen_echo
from datetime import datetime
app = Flask(__name__) 

SERVE_CONTENT_TYPE = ['html', 'txt', 'pdf', 'js', 'png', 'css', 'jpg', 'mp4']
SERVE_CONTENT_PREFIX = 'example'
IMG_TMP_DIR='/tmp'

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
    response_obj = make_response( render_template('debug.html', pd=pd) )
    response_obj.status_code = status_code
    return response_obj

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
 

@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory('static/', 'index.html')

   
@app.route('/site/shop/')
@app.route('/site/shop/<path:path>')
def stupid_site_shop(path=''):
    rpath=path
    if path=='':
        rpath='home.html'
    ret_body = send_from_directory('static/site/shop/', rpath)
    return stupid_respond_filter(ret_body)
  
@app.route('/<anystr>/<subpath>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE'])
def stupid_routing(anystr, subpath):
    
    if request.method == 'POST' or request.method == 'PUT':
        app.logger.debug('url: {} {}'.format(request.method, request.url))
        app.logger.debug('content-type: {}'.format(request.content_type))
        app.logger.debug('content-length: {}'.format(request.content_length))
        app.logger.debug('data: {}'.format(request.data))
        app.logger.debug('form: {}'.format(request.form))
        app.logger.debug('files: {}'.format(request.files))
        if 'data' in request.files:
            file = request.files['data']
            file.save('/tmp/tmp.dat')

    m=re.search('^(\d+)x(\d+)\.(jpg|png|gif)$', subpath)
    if m is not None:
        return serve_boximg(subpath)

    elif re.search(r'^([45]\d{2})\..+$', subpath):
        return serve_intentional_error(subpath)
    
    elif re.search(r'echo\.(txt|html|json|js|css|xml|jpg|png|gif)$', subpath):
        return serve_echo_content(subpath)

    # other than that
    return serve_example(subpath)
    

#interface
def serve_content(subpath):
    '''
    returns Response object
    '''
    pass

def serve_boximg(subpath):
    m=re.search('^(\d+)x(\d+)\.(jpg|png|gif)$', subpath)
    if m is None:
        return 'Invalid Path', 404
    try:
        w=int(m.group(1))
        h=int(m.group(2))
        ext=m.group(3)
    except Exception as err:
        return 'Invalid Path', 404
    if w > 4096 or h > 4096:
        return 'width and heigh must be [1-4096]', 404
    if w < 1 or w < 1:
        return 'width and heigh must be [1-4096]', 404

    if not os.path.exists( os.path.join(IMG_TMP_DIR, subpath)):
        print('new img generated: {}', os.path.join(IMG_TMP_DIR, subpath))
        imgen((w,h), ext, IMG_TMP_DIR)
    ret_body = send_from_directory(IMG_TMP_DIR, subpath)
    return stupid_respond_filter(ret_body)

def serve_intentional_error(subpath):
    prefix = re.search(r'^([45]\d{2})\..+$', subpath)
    if prefix is not None:
        response_obj = makeIntentErrRes( int(prefix.group(1)) )
        return stupid_respond_filter(response_obj)

def serve_echo_content(subpath):
    response_dict = dict()
    
    response_dict['request_headers'] = DictHeaders(request.headers) 
    response_dict['connecting-ip'] = request.remote_addr
    response_dict['url'] = '{} {}'.format(request.method, request.url)
    response_dict['date'] = '{}'.format(datetime.now())
    
    prefix, ext = os.path.splitext(subpath)
    response_obj=Response()
    if ext in ('.txt', '.html', '.json', '.js', '.css', '.xml'): 
        response_obj = make_response( json.dumps(response_dict, indent=2) )
        if subpath.endswith('txt'):
            response_obj.mimetype = 'text/plain'
        elif subpath.endswith('html'):
            response_obj.mimetype = 'text/html'
        elif subpath.endswith('json'):
            response_obj.mimetype = 'application/json'
        elif subpath.endswith('js'):
            response_obj.mimetype = 'application/javascript'
        elif subpath.endswith('xml'):
            response_obj.mimetype = 'application/xml'
        elif subpath.endswith('css'):
            response_obj.mimetype = 'text/css'
        else:
            response_obj.mimetype = 'text/plain'

    elif ext in ('.jpg','.png', '.gif'):
        rnd=random.randint(0,1000)
        imgen_echo(json.dumps(response_dict, indent=2), fmt=ext[1:], outdir=IMG_TMP_DIR, fileprefix=str(rnd))
        response_obj = send_from_directory(IMG_TMP_DIR, '{}{}'.format(rnd, ext))



    return stupid_respond_filter(response_obj)

def serve_example(subpath):
    ret_body = send_from_directory('static/', subpath)
    return stupid_respond_filter(ret_body)



def stupid_respond_filter(response_obj):
    if 'Set-Status-Code' in request.args.keys():
        query_val = re.search(r'^([456789]\d{2})$', request.args['Set-Status-Code'])
        if query_val is not None:
            response_obj.status_code = int(query_val.group(1)) 

    if 'Set-Status-Code' in request.headers:
        header_val = re.search(r'^([456789]\d{2})$', request.headers['Set-Status-Code'])
        if header_val is not None:
            response_obj.status_code = int(header_val.group(1))

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
    
    # appending response header from query strings
    for k,v in request.args.items():
        if v == '':
            del response_obj.headers[k]
        else:
            response_obj.headers[k]=v

    # appending response header from request header "ResHeader" json format
    if 'Set-Response-Header' in request.headers:
        try:
            hdr = json.loads( request.headers['Set-Response-Header'] )
            for k,v in hdr.items():
                if k == 'Set-Cookie':
                    c=v.split('=')
                    ckey=c[0]
                    cval=c[1]
                    print(c)
                    response_obj.set_cookie(ckey, value=cval)
                elif v == '':
                    del response_obj.headers[k]
                else:
                    response_obj.headers[k]=v
        except Exception as err:
            pass

    res_hdr = json.dumps( DictHeaders(response_obj.headers) )
    response_obj.headers['Request-Headers']=req_hdr
    response_obj.headers['Response-Headers']=res_hdr
    response_obj.headers['Request-Cookies']=req_cookie
    response_obj.headers['Connection-IP']=request.remote_addr
    return response_obj


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
