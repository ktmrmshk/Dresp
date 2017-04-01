# Dresp
A web server serving stupid responses


```
Your Browser                           Stupid Responder
(client)                               (Dress) as an Origin Server

+--------------+ * Query Strings      +------------------------------------+
|              | * Requesst Headers   |                                    |
|    requrst1  | +----------------------------------+                      |
|              |                      |             v                      |
|              |    w/ Intentional    |   * Generating response headers    |
|              |    Response Header   |             +                      |
|    response1 | <----------------------------------+                      |
+--------------+                      |                                    |
                                      |                                    |
+--------------+                      |                                    |
|              |  * /foobar/4xx.html  |                                    |
|    request2  | +----------------------------------+                      |
|              |                      |             v                      |
|              |                      |   * Generating 4xx/5xx response    |
|              |  Intentional 4xx page|             +                      |
|    response2 | <----------------------------------+                      |
+--------------+                      |                                    |
                                      +------------------------------------+

```

# Installation

## from Dockerhub (easiest way)

Open termial on a machine docker's installed, and

```
# docker run -d -p 8080:5000 ktmrmshk/dresp bash /drespstart.sh
```

Then, open your browser and access to this server like `http://to.this.server.com:8080/`.


## from Dockerfile

From this git repository,

```
# git clone https://github.com/ktmrmshk/Dresp.git
# cd Dresp
# docker build -t dresp .
# docker run -d -p 8080:5000 dresp bash /drespstart.sh   
```


## from source

work in progress....


# Usage

## Accessing Objects

Stupid Responder (Rresp) serves following content:

* file_prefix: example
* file_type: html, txt, pdf, js, png, css, jpg, mp4

For instance, you can get jpeg file by "http://to.this.server.com/YourPath/example.jpg".

The middle of full-path "YourPath" can be set any string you want, because this path string
is ignored in the servering process.

Here are examples of the path to each content:

* http://to.dresp.server.com/YourPath/example.jpg
* http://to.dresp.server.com/FooBar/example.html
* http://to.dresp.server.com/ABC123/example.txt
* http://to.dresp.server.com/HiLows/example.pdf
* http://to.dresp.server.com/AbcXyz/example.js
* http://to.dresp.server.com/XXXXXX/example.png
* http://to.dresp.server.com/123456/example.css
* http://to.dresp.server.com/hogepo/example.mp4

## Set-up Favorite Response Headers w/ Query Strings

You can set-up favorite respinse headers using query string on a request.
Formt is like `?Your-Header=your-value&Cache-Control=no-store`, then you get
objects with response header including:

* `Your-Header: your-value`
* `Cache-Control: no-store`

If you want to delete specific response header, pass the query without any value.
e.g. to delete `Cache-Control` header, pass the request with query like `?Cache-Control=`.

### Examples

* http://to.dresp.server.com/YourPath/example.jpg?Cache-Control=no-cache&Vary=User-Agent
* http://to.dresp.server.com/YourPath/example.jpg?Edge-Control=no-store


## Set-up Favorite Response Headers w/ Requrst Header

Also, setting up response header can be done by `Set-Response-Header` request header with json formatted data, like:

* `Set-Response-Header: {"abc":123, "Edge-Control":"no-store"}`


## Checking request / response headers at this server catch

Dresp returns debuging info as a json data in response header as follows:

* `Request-Headers`
* `Request-Cookies`
* `Response-Headers`


## Getting Intentional 4xx/5xx response 

You get intentional 4xx/5xx response by accessing 

* http://to.dresp.server.com/hogepo/403.html
* http://to.dresp.server.com/hogepo/503.html

Dresp returns the any 4xx/5xx response status you need.

# Directory

Representive paths:

* http://to.dresp.server.com/ : Top page (including help)
* http://to.dresp.server.com/index.html : Top page (including help)

* http://to.dresp.server.com/hogepo/example.jpg : jpeg object page
* http://to.dresp.server.com/hogepo/example.html : html object page

* http://to.dresp.server.com/hogepo/403.html : Intentional 403 error page


