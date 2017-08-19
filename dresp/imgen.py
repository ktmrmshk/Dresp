from PIL import Image, ImageDraw
import os

def imgen(size, fmt='jpg', outdir='./'):
    outfile='{}x{}.{}'.format(size[0], size[1], fmt)
    img = Image.new('RGB', size, (210,210,210))
    d=ImageDraw.Draw(img)
    d.text((0,0), outfile, (0,0,0))
    img.save(os.path.join(outdir,outfile))

if __name__ == '__main__':
    imgen((20, 10), 'png')

