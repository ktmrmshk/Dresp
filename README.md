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