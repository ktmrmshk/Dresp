from PIL import Image, ImageDraw, ImageFont
import os

def imgen(size, fmt='jpg', outdir='./'):
    outfile='{}x{}.{}'.format(size[0], size[1], fmt)
    img = Image.new('RGB', size, (210,210,210))
    d=ImageDraw.Draw(img)
    d.text((0,0), outfile, (0,0,0))
    img.save(os.path.join(outdir,outfile))

def imgen_echo(txt, fmt='jpg', outdir='./', fileprefix='tmp123'):
    outfile='{}.{}'.format(fileprefix, fmt)

    #load font
    font = ImageFont.truetype('static/CourierNew.ttf', 18)
    
    img = Image.new('RGB', (3200,1600), (210,210,210))
    d=ImageDraw.Draw(img)
    d.multiline_text((0,0), txt, (0,0,0), font=font)
    img.save(os.path.join(outdir,outfile))

import json
if __name__ == '__main__':
    imgen((20, 10), 'png')
    
    raw='''{"Host": "localhost:5000", "Connection": "keep-alive", "Pragma": "akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-get-request-id", "Cache-Control": "no-cache", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,ja;q=0.8", "X-Im-Piez": "on", "X-Akamai-Ro-Piez": "on", "X-Akamai-A2-Disable": "on", "Show-Akamai-Debug-4Fbgbadszg": "true", "X-Akamai-Device-Characteristics": "abc123"}'''
    imgen_echo(json.dumps(json.loads(raw),indent=2), 'png')



