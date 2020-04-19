# **Packet Responder Project** [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://gitlab.com/limner/network-project-3962)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)
![Build](https://img.shields.io/bitbucket/pipelines/atlassian/adf-builder-javascript/task/SECO-2168.svg)
![PyPI - Status](https://img.shields.io/pypi/status/Django.svg)
![Read the Docs](https://img.shields.io/readthedocs/pip.svg)

This is Packet Resoinder with only python Which reply to ARP-DNS-ICMP Packets.

Version : 1.6

Build : Passing

Author : Amir Masoud Noohi

Language : Python Both 2.7 - 3.7.0




# **PreRequirements**

For This Project You Need below Requirements :
- pyhon3

```shell
$ apt install python3
```

# **Usage**
## Step0 : Cloning

First of All Clone the Project : 

```shell
$ git clone https://gitlab.com/limner/network-project-3962.git
$ cd network-project-3962/2
```

## Step1 : Run Code

This Code Consist of 3 Part : 

1- ARP : We recv All packets and after we receive arp request we create arp reply packet and send it to arp sender 
for example :

```shell
$ python3 main.py -t arp -i eth0
```

2- ICMP : in this type we recv All packets and then reply to packets which is icmp request . icmp reply packet has two parameter which is type of icmp packet and the code of that


```shell
$ python3 main.py -t icmp -i eth0 -d 0,0
```

3- DNS : in this type of responder when we receive any dns request then we create new dns reply packet with empty data and then we send it to sender : 

```shell
$ python3 main.py -t dns -i eth0
```
## ARP
![pic_arp](http://uupload.ir/files/ehs6_3-arp.png)

## ICMP
![pic_icmp](http://uupload.ir/files/lfdt_3-icmp.png)

## DNS
![pic_dns](http://uupload.ir/files/6r7_3-dns.png)


# **Run-Time**
## ARP
![RUN GIF](https://highhost.org/gif-video/3-arp.gif)

## ICMP
![RUN GIF](https://highhost.org/gif-video/3-icmp.gif)

![RUN GIF](https://highhost.org/gif-video/3-dns.gif)


# **Files**

- <a href="https://gitlab.com/limner/network-project-3962/blob/master/3/main.py" target="_blank">`/main.py`</a> : This is Main File
- <a href="https://gitlab.com/limner/network-project-3962/blob/master/3/extra.py" target="_blank">`/extra.py`</a> : This is sniffer code that is embeded in main.py


# **Support**

Reach out to me at one of the following places!

- Telegram at <a href="https://t.me/amirmnoohi" target="_blank">@amirmnoohi</a>
- Gmail at <a href="mailto:highlimner@gmail.com" target="_blank">highlimner@gmail.com</a>

# **License**

[![License](https://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2018 © <a href="https://gitlab.com/limner/network-project-3962" target="_blank">Network Project</a>.
