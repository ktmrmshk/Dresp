Dresp: Stupid Responder
=======================

See https://github.com/ktmrmshk/Dresp to learn more.

## Sample Content

* html - [/foobar123/example.html](./foobar123/example.html)
* css - [/foobar123/example.css](./foobar123/example.css)
* js - [/foobar123/example.js](./foobar123/example.js)
* json - [/foobar123/example.json](./foobar123/example.json)
* txt - [/foobar123/example.txt](./foobar123/example.txt)
* jpg - [/foobar123/example.jpg](./foobar123/example.jpg)
* png - [/foobar123/example.png](./foobar123/example.png)
* webp - [/foobar123/example.webp](./foobar123/example.webp)
* svg - [/foobar123/example.svg](./foobar123/example.svg)
* ttf - [/foobar123/example.ttf](./foobar123/example.ttf)
* woff - [/foobar123/example.woff](./foobar123/example.woff)
* woff2 - [/foobar123/example.woff2](./foobar123/example.woff2)
* mp4 - [/foobar123/example.mp4](./foobar123/example.mp4)
* webm - [/foobar123/example.webm](./foobar123/example.webm)

* example site - [/site/shop/](./site/shop/)

* Custom Header / Response Status Code
  - `Cache-Control: no-store` (by query string) - [/foobar123/example.html?Cache-Control=no-store](./foobar123/example.html?Cache-Control=no-store)
  - `403` Response (by filename) - [/abc123/403.html](./abc123/403.html)
  - `529` Response (by filename) - [/hello/529.html](./hello/529.html)
  - `403` Response (by query string) - [/foobar123/example.json?Set-Status-Code=403](./foobar123/example.json?Set-Status-Code=403)
  - `Vary: User-Agent` + `403` Response - [/foobar123/example.json?Vary=User-Agent&Set-Status-Code=403](./foobar123/example.json?Vary=User-Agent&Set-Status-Code=403)
  - `301` Redirect to `https://abc.com/` - [/hoge/example.html?Set-Status-Code=301&Location=https://abc.com/](./hoge/example.html?Set-Status-Code=301&Location=https://abc.com/)

* Multi Redirects
  - Redirect to `/foo123/redirect/302/9` - [/foo123/redirect/302/10](./foo123/redirect/302/10)
  - Redirect to `/foo123/redirect/302/8` - [/foo123/redirect/302/9](./foo123/redirect/302/9)
  - Redirect to `/foo123/redirect/302/7` - [/foo123/redirect/302/8](./foo123/redirect/302/8)
  - ....

* Delayed Response
  - 2.5 sec delayed response - [/foo123/example.html?Set-Response-Delay=2.5](./foo123/example.html?Set-Response-Delay=2.5)


* Specific Sized Images
  - JPG of 640x480 - [/foobar/640x480.jpg](./foobar/640x480.jpg)
  - png of 640x480 - [/abc123/640x480.png](./abc123/640x480.png)
  - gif of 100x100 - [/anystr/100x100.gif](./anystr/100x100.gif)

* Echo mode response
  - [/foobar/echo.txt](./foobar/echo.txt)
  - [/foobar/echo.html](./foobar/echo.html)
  - [/foobar/echo.json](./foobar/echo.json)
  - [/foobar/echo.css](./foobar/echo.css)
  - [/foobar/echo.xml](./foobar/echo.xml)
  - [/foobar/echo.jpg](./foobar/echo.jpg)
  - [/foobar/echo.png](./foobar/echo.png)
  - [/foobar/echo.gif](./foobar/echo.gif)





