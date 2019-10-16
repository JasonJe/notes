## 6.5 中间件-`Nginx`

>date: 2019-05-15

![](../assets/images/65.jpg)

### 6.5.1 概述

`Nginx`是一个异步框架的`Web`服务器，也可以用作反向代理，负载平衡器和请求分发。

`Nginx`通过异步非阻塞的事件处理机制实现高并发。`Apache`每个请求独占一个线程，非常消耗系统资源。

事件驱动适合于`IO`密集型服务(`Nginx`)，多进程或线程适合于`CPU`密集型服务(`Apache`)，所以`Nginx`适合做反向代理，而非`Web`服务器使用。

* `I/O`模型

`Nginx`采用的`I/O`模型是`epoll`。每当`FD`就绪，就采用系统的回调函数将`FD`放入，效率更高，最大连接无限制。

* 进程模型

`Nginx`服务的运行一般存在`master process`（监控进程，也叫做主进程）和`woker process`（工作进程），还可能有`cache`相关进程。 

![进程模型](../assets/images/651_01.png)

1. `master`进程

监控进程充当整个进程组与用户的交互接口，同时对进程进行监护。

它不需要处理网络事件，不负责业务的执行，只会通过管理`worker`进程来实现重启服务、平滑升级、更换日志文件、配置文件实时生效等功能。

`master`进程中`for(::)`无限循环内有一个关键的`sigsuspend()`函数调用，该函数调用使得`master`进程的大部分时间都处于挂起状态，直到`master`进程收到信号为止。

2. `worker`进程

基本的网络事件，是放在`worker`进程中来处理的，`worker`之间的进程是对等的，只可能在相同的`worker`中处理，一个`worker`进程不可能处理其他进程的请求。 

`worker`的个数，**一般设置成与`CPU`的个数相同**。

太多的`worker`数，只会导致进程相互竞争`CPU`资源，从而带来不必要的上下文切换。

每个`worker`进程从`master`进程`fork`过来，它们继承了父进程`master`的所有属性，当然也包括已经建立好的`socket`(`listenfd`)，但`socket`并不是同一个，只是每个进程的`socket`会监控在同一个`ip`地址与端口。

所有`worker`进程的`listenfd`会在新连接到来时变得可读，为保证只有一个进程处理该连接，所有`worker`进程在注册`listenfd`读事件前抢`accept_mutex`，抢到互斥锁的那个进程注册`listenfd`读事件，在读事件里调用`accept`接受该连接。

这种进程模型的**优点：**

a. 每个`worker`进程独立，不需加锁，省去锁操作的开销；

b. 独立的进程保证进程间互不干扰，服务不中断。

* `connection`

`Nginx`中每个进程的连接数都有一个最大上限，其大致等于系统的**最大句柄数(`ulimit -n`) - 已经打开的`socket`连接数**。

`Nginx`通过`worker_connections`来设置**每个进程支持的最大连接数**，其实现是通过连接池进行管理的，每个`worker`都独立一个连接池，其大小为`worker_connections`，其实际为`worker_connections`大小的`ngx_connection_t`（`nginx`对连接的封装）数组。同时，还存在一个`free_connections`来保存空闲的`ngx_connection_t`，每获取一个连接时候，就从中获取一个，用完再放回。

`Nginx`其作为反向代理服务器时，能进行的最大并发数为` worker_connections * worker_processes/2 `， 因为每个并发会建立与客户端的连接和与后端服务的连接，会占用两个连接。

* 惊群现象

多进程（多线程）在同时阻塞等待同一个事件的时候（休眠状态），如果等待的这个事件发生，那么他就会唤醒等待的所有进程（或者线程），但是最终却只可能有一个进程（线程）获得这个时间的控制权，对该事件进行处理，而其他进程（线程）获取控制权失败，只能重新进入休眠状态，从而造成性能的浪费。

一般来说，当一个连接进来后，所有在这个`socket`上面`accept`的进程，都会收到通知，而只有一个进程可以成果`accept`这个连接，其它的则`accept`失败。

`Nginx`采用`accept-mutex`来解决惊群问题：当一个请求到达的时候，只有竞争到锁的`worker`进程才会惊醒处理请求，其他进程会继续等待，结合`timer_solution`配置的最大的超时时间继续尝试获取`accept-mutex`。

### 6.5.2 静态资源`Web`服务

`Nginx`将网络路径(域名)和本地路径进行了映射，即当通过`url`路径访问静态资源时，`Nginx`根据映射地址找到资源文件位置，然后到这个特定的位置拿到静态资源，然后返回，响应给客户端。

基于上述，其对静态文件、索引文件的自动索引效率特别高，同时`Nginx`的`I/O`模型使其进行静态处理时候性能特别高。

```
server {
            listen       80;                                                         
            server_name  www.xxx.com; # 静态网站访问的域名地址                                            
            client_max_body_size 1024M;
            location / { # 直接静态项目的绝对路径的根目录
                root   /var/www/xxx_static;
                index  index.html;
            }
        }
```

### 6.5.3 代理服务

* 反向代理和正向代理

正向代理是代理客户端，为客户端收发请求，使真实客户端对服务器不可见；而反向代理是代理服务器端，为服务器收发请求，使真实服务器对客户端不可见。

反向代理(`Reverse Proxy`)方式是指以代理服务器来接受`Internet`上的连接请求，然后将请求转发给内部网络上的服务器，并将从服务器上得到的结果返回给`Internet`上请求连接的客户端，此时代理服务器对外就表现为一个服务器。

反向代理的作用

1. 保护网站安全：任何来自`Internet`的请求都必须先经过代理服务器；

2. 通过配置缓存功能加速`Web`请求：可以缓存真实`Web`服务器上的某些静态资源，减轻真实`Web`服务器的负载压力；

3. 实现负载均衡：充当负载均衡服务器均衡地分发请求，平衡集群中各个服务器的负载压力。

`Nginx`的网络模式是事件驱动，其能在多个`I/O`句柄中快速切换，针对`I/O`密集型的工作更加得心应手。如在反向代理中，其在客户端和`Web`应用之间只起到数据中转的作用，这里只存在纯粹的`I/O`操作。

```
server {
    listen 80;
    server_name  www.outside.com; # 访问的域名地址 

    location / {
        proxy_pass http://www.inside.com; # 将域名地址的请求转发到实际的地址
    }
}
```

正向代理：如果把局域网外的`Internet`想象成一个巨大的资源库，则局域网中的客户端要访问`Internet`，则需要通过代理服务器来访问才能访问得到，这种代理服务就称为正向代理。

```
# 假设此服务器能访问公网，IP为192.168.1.222
server {  
    resolver 114.114.114.114; # 指定DNS服务器IP地址  
    listen 8080;  
    location / {  
        proxy_pass http://$http_host$request_uri; # 设定代理服务器的协议和地址  
    }  
}  
```

其它不能访问公网的服务器通过设置代理的方式访问公网，如下：

```
# curl -x 192.168.1.222:8080 -I http://xxxx.xxxx.xxxx/xxx.xxx
```

### 6.5.4 负载均衡

在反向代理的基础上，`Nginx`实现负载均衡变得十分简单，依赖于`Nginx`的`ngx_http_upstream_module`模块，其可以实现多种转发策略。

```
# 1 默认采用轮询(Round-Robin)的方式将请求转发到组中服务器
http {
    upstream app_group { # 定义一个后端的服务器组，命名为app_group
        server 192.168.56.102;
        server 192.168.56.103;
        server 192.168.56.104;
    }

    server {
        listen 80;
        server_name  www.example.com;

        location / {
            proxy_pass http://app_group;
        }
    }
}

# 2 最少连接(Least-connected)策略，在该策略下会尝试避繁忙的机器，将请转到有减少连接较少的机器上，该策略可以环节呢后端服务器负载冷热不均的问题
upstream app_group {
    least_conn;
    server 192.168.56.102;
    server 192.168.56.103;
    server 192.168.56.104;
}

# 3 最少耗时(Least-time)策略：该策略会将请求转到都具有最小平均影响时间和最少活动链接的后端服务器
upstream app_group {
    least_time;
    server 192.168.56.102;
    server 192.168.56.103;
    server 192.168.56.104;
}

# 4 回话保持(Session persistence)策略，在轮询或者最少连接策略下，同一个用户(同一个客户端IP)的不同请求会随机分配到不同的后端服务器上。回话保持策略会通过客户端 IP 计算一个成 Hash 值，按照 hash 值分配后端服务器，该策略可以使得同一个用户的请求落在同一个后端主机上
upstream app_group {
    ip_hash;
    server 192.168.56.102;
    server 192.168.56.103;
    server 192.168.56.104;
}

# 5 自定义 Hash 策略，前面介绍的回话保持策略通过客户端IP计算 hash 值，自定义 hash 策略可以根据用户自己定的主键计算hash值，比如使用 uri 作为 key 计算hash，同时还可以指定可选参数来选择使用何种 hash 算法

upstream app_group {
    hash $request_uri;
    server 192.168.56.102;
    server 192.168.56.103;
    server 192.168.56.104;
}

# 6 基于权重策略，Nginx 可以为不同的主机配置不同的权重，按照权重比例转发流量
upstream app_group {
    server 192.168.56.102 weight=3;
    server 192.168.56.103;
    server 192.168.56.104;
}
```

### 6.5.5 缓存服务

`Nginx`的`http_proxy`模块，可以对客户已经访问过的内容在`Nginx`服务器本地建立副本，在一段时间内再次访问该数据，就不需要通过`Nginx`服务器再次向后端服务器发出请求，所以能够减少`Nginx`服务器与后端服务器之间的网络流量，减轻网络拥塞，同时还能减小数据传输延迟，提高用户访问速度。同时，当后端服务器宕机时，`Nginx`服务器上的副本资源还能够相应相关的用户请求，这样能够提高后端服务器的鲁棒性。

```
proxy_temp_path /var/tmp/nginx/proxy; #  缓存临时目录

# proxy_cache_path 设置缓存目录，目录里的文件名是 cache_key 的MD5值
# levels=1:2 keys_zone=cache_one:50m 表示采用2级目录结构，Web缓存区名称为cache_one，内存缓存空间大小为100MB，这个缓冲zone可以被多次使用
# inactive=1d max_size=5g 表示2天没有被访问的内容自动清除，硬盘最大缓存空间为2GB，超过这个大学将清除最近最少使用的数据
proxy_cache_path /var/tmp/nginx/cache levels=1:2 keys_zone=cache_one:20m inactive=1d max_size=5g;

server {

 listen  80;
 server_name localhost;

 root /var/www;

 location ~ \.(jpg|png|jpeg|gif|css|js)$ {
  proxy_cache cache_one; # 引用前面定义的缓存区 cache_one

  proxy_cache_valid 200 304 12h; #  为不同的响应状态码设置不同的缓存时间，比如200、302等正常结果可以缓存的时间长点，而404、500等缓存时间设置短一些，这个时间到了文件就会过期，而不论是否刚被访问过

  proxy_cache_key $host$uri$is_args$args; # 定义cache_key
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-For $remote_addr;
  proxy_pass http://127.0.0.1:8181;
  proxy_set_header X-Forwarded_For $proxy_add_x_forwarded_for;
  expires 1d;
 }
}
```

### 6.5.6 限流

`Nginx`接入层的限流可以使用`Nginx`自带了两个模块：连接数限流模块`ngx_http_limit_conn_module`和漏桶算法实现的请求限流模块`ngx_http_limit_req_module`。

```
http {
    # 针对每个变量(这里指IP，即$binary_remote_addr)定义一个存储session状态的容器。这里定义了一个20m的容器，按照32bytes/session，可以处理640000个session
    limit_zone one  $binary_remote_addr  20m;
    # rate是请求频率. 每秒允许12个请求
    limit_req_zone  $binary_remote_addr  zone=req_one:20m rate=12r/s;
    # 表示一个IP能发起10个并发连接数
    limit_conn   one  10;
    # 与limit_req_zone对应。burst表示缓存住的请求数
    limit_req   zone=req_one burst=120;
    server  {
            listen          80;
            server_name     status.xxx.com ;
            location / {
                    stub_status            on;
                    access_log             off;
            }
    }
}
```