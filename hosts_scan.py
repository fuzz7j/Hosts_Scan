#!/usr/bin/python3
# coding: utf-8

import requests
import re
import argparse
import threading
import dns.resolver

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str, help="IP file")
    parser.add_argument('-s', '--subdomain', type=str, help="Subdomain file")
    parser.add_argument('-d', '--domain', type=str, help="Domain file")
    parser.add_argument('-T', '--threads', type=int, default=20, help="Threads, Default 20")
    return parser.parse_args()

def host_check(host):
    try:
        dns.resolver.Resolver().resolve(host, "A")
        return host
    except Exception:
        err = '[-]{} 解析失败'.format(host)
        logger(err)


def host_scan(ip, host):
    blacklist = ["抱歉，站点已暂停","Apache HTTP Server Test Page powered by CentOS","Test Page for the Nginx HTTP Server on Red Hat Enterprise Linux","Test Page for the Nginx HTTP Server on Fedora","IIS","HTTP Server Test Page","Test Page for the Nginx HTTP Server on Fedora","400 No required SSL certificate was sent","Page not found at /","Not Found","Welcome to CentOS","Site not found","没有找到站点","HTTP Status 404 – Not Found","IIS7","页面找不到","Welcome to tengine!","网站未发布","421 Misdirected Request","网站访问报错","IIS Windows Server","Welcome to OpenResty!","500 Internal Server Error", "410 Gone", "503 Service Temporarily Unavailable", "403.1 - 禁止访问: 执行访问被拒绝。", "Welcome to penRestOy!", "404 Not Found", "Welcome to nginx!", "403 Forbidden", "502 Bad Gateway"]
    schemes = ["http://", "https://"]
    host = host_check(host)
    if host != None:
        for scheme in schemes:
            url = scheme + ip
            headers = {'Host':host.strip(),'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            try:
                s = requests.session()
                requests.packages.urllib3.disable_warnings()
                res = s.get(url, verify=False, headers=headers, timeout=3)
                res.encoding = 'utf-8'
                title = ""
                try:
                    title = re.search('<title>(.*)</title>', res.text).group(1)
                except Exception as e:
                    title = u'获取标题失败'
                if (title == "获取标题失败" and len(res.text) <= 300) or title in blacklist:
                    info = '[-]{} || {} || {} || {} || {}'.format(ip,host,scheme+host,len(res.text), title)
                    logger(info)
                else:
                    info = '[+]{} || {} || {} || {} || {}'.format(ip,host,scheme+host,len(res.text), title)
                    logger(info)
            except Exception as e:
                err = '[-]{} || {} || {} || {}'.format(ip, host, scheme+host, '访问失败')
                logger(err)

def logger(result):
    print(result)
    if result[:3] == '[+]':
        with open('result.txt', 'a+') as f:
            f.write('%s\n' % result[3:])
    elif result[:3] == '[-]':
        with open('log.txt', 'a+') as f:
            f.write('%s\n' % result[3:])

def file_parse(filename):
    with open(filename, 'r') as file:
        text_temp = file.read().split('\n')
    if text_temp == None:
        return None
    text_temp = list(set(text_temp))
    texts = []
    for text in text_temp:
        if text != '':
            texts.append(text)
    return texts

class thread(threading.Thread):
    def __init__(self,func,args,sem):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.sem = sem
    def run(self):
        self.func(*self.args)
        self.sem.release()

if __name__ == '__main__':
    args = parse_args()
    if args.ip != None and args.subdomain != None and args.domain != None:
        sem = threading.Semaphore((args.threads))
        ips = file_parse(args.ip)
        subdomains = file_parse(args.subdomain)
        domains = file_parse(args.domain)

        for ip in ips:
            for subdomain in subdomains:
                for domain in domains:
                    sem.acquire()
                    t = thread(host_scan, args=(ip, subdomain + '.' + domain), sem=sem)
                    t.start()