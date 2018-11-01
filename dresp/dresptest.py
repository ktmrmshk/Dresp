import unittest
import requests
import json

class TestPOST(unittest.TestCase):
    def test_foobar(self):
        self.assertTrue(1==1)

class TestDresp(unittest.TestCase):
    def setUp(self):
        self.url='http://localhost:5000'
    def tearDown(self):
        pass

    def test_4xx_path(self):
        code=405
        r=requests.get( '{}/foobar/{}.html'.format(self.url, code) )
        self.assertEqual(r.status_code, code)
        self.assertTrue('Intentional' in r.text)

    def test_5xx_path(self):
        code=502
        r=requests.get( '{}/foobar/{}.html'.format(self.url, code) )
        self.assertEqual(r.status_code, code)
        self.assertTrue('Intentional' in r.text)

    def test_4xx_query(self):
        code=421
        r=requests.get( '{}/foobar/example.html?Set-Status-Code={}'.format(self.url, code) )
        self.assertEqual(r.status_code, code)
    
    def test_5xx_query(self):
        code=521
        r=requests.get( '{}/foobar/example.html?Set-Status-Code={}'.format(self.url, code) )
        self.assertEqual(r.status_code, code)
   
    def test_4xx_hdr(self):
        code=405
        r=requests.get( '{}/foobar/example.html'.format(self.url), headers={'Set-Status-Code' : str(code)} )
        self.assertEqual(r.status_code, code)

    def test_5xx_hdr(self):
        code=505
        r=requests.get( '{}/foobar/example.html'.format(self.url), headers={'Set-Status-Code' : str(code)} )
        self.assertEqual(r.status_code, code)

    def test_static_content(self):
        for ext in ('jpg', 'html', 'txt', 'pdf', 'js', 'png', 'css', 'mp4'):
            r=requests.get( '{}/foobar/example.{}'.format(self.url, ext))
            self.assertEqual(r.status_code, 200)
            self.assertTrue('Request-Headers' in r.headers)
            self.assertTrue('Request-Cookies' in r.headers)
            self.assertTrue('Response-Headers' in r.headers)
            self.assertTrue('Connection-IP' in r.headers)

    def test_index_page(self):
        for f in ('/', '/index.html'):
            r=requests.get( '{}{}'.format(self.url, f))
            self.assertEqual(r.status_code, 200)
    
    def test_favorite_response_hdr_by_query(self):
        f_hdr={'yourname':'Akam-Taro', 'age':'123'}
        f_hdr_q = list() 
        for k,v in f_hdr.items():
            f_hdr_q.append('{}={}'.format(k,v))
        query='?' + '&'.join(f_hdr_q)
        
        r=requests.get( '{}/foobar/example.html{}'.format(self.url, query))
        for k,v in f_hdr.items():
            self.assertTrue( r.headers[k] == v)
        #print(r.headers)

    def test_favorite_response_hdr_by_hdr(self):
        f_hdr={'yourname':'Akam-Taro', 'age':'123'}
        hdr = {'Set-Response-Header': json.dumps(f_hdr)}
        r=requests.get( '{}/foobar/example.html'.format(self.url), headers=hdr)
        for k,v in f_hdr.items():
            self.assertTrue( r.headers[k] == v)


    def test_redirect_by_query(self):
        codes=[301, 302, 307]
        for code in codes:
            query='?Set-Status-Code={}&Location=http://www.abc.com'.format(code)
            r=requests.get( '{}/foobar/example.html{}'.format(self.url, query), allow_redirects=False)
            self.assertEqual(r.status_code, code)
            self.assertEqual(r.headers['Location'], 'http://www.abc.com')
            self.assertTrue(r.is_redirect)


    def test_redirect_by_hdr(self):
        codes=[301, 302, 307]
        for code in codes:
            hdr={'Set-Response-Header': '{"Location": "http://www.abc.com"}', 'Set-Status-Code': str(code)}
            r=requests.get( '{}/foobar/example.html'.format(self.url), headers=hdr, allow_redirects=False)
            self.assertEqual(r.status_code, code)
            self.assertEqual(r.headers['Location'], 'http://www.abc.com')
            self.assertTrue(r.is_redirect)
    
    def test_demo_web_site(self):
        r=requests.get( '{}/site/shop/'.format(self.url) )
        self.assertEqual(r.status_code, 200)
        self.assertTrue( 'text/html' in r.headers['Content-Type'])
    
    def test_arbitrary_size_images(self):
        files=('100x100.jpg', '640x480.png', '120x120.gif')
        for f in files:
            r=requests.get( '{}/site/{}'.format(self.url, f))
            self.assertEqual( r.status_code, 200 )
            self.assertTrue( 'image/' in r.headers['Content-Type'] )
    
    def test_echo_img(self):
        files=('echo.jpg', 'echo.png', 'echo.gif')
        for f in files:
            r=requests.get( '{}/foobar/{}'.format(self.url, f))
            self.assertEqual( r.status_code, 200 )
            self.assertTrue( 'image/' in r.headers['Content-Type'] )

    def test_echo_text(self):
        files=('echo.txt', 'echo.html', 'echo.css')
        for f in files:
            r=requests.get( '{}/foobar/{}'.format(self.url, f))
            self.assertEqual( r.status_code, 200 )
            self.assertTrue( 'text/' in r.headers['Content-Type'] )

    def test_echo_text(self):
        files=('echo.js', 'echo.json', 'echo.xml')
        for f in files:
            r=requests.get( '{}/foobar/{}'.format(self.url, f))
            self.assertEqual( r.status_code, 200 )
            self.assertTrue( 'application/' in r.headers['Content-Type'] )





if __name__ == '__main__':
    unittest.main()


