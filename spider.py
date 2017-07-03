import random
import re
import time

import requests


class ProxyHandler(object):
    '''
     使用代理增加文章阅读量(类似于csdn的博客里面的阅读数)
     '''

    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.9 NetType/4G Language/zh_CN"
        ]
        # 获取代理地址的网址
        self.proxy_get_url = 'http://www.xicidaili.com'
        # 目标地址
        self.visit_url = 'https://mp.weixin.qq.com/s/pfCr5Lj4MCy4x_7zJowLxA'
        # 获取能用的代理集合
        self.proxy_list = []
        # 请求超时时间为3s
        self.timeout = 3

    def get_proxy_list(self):
        '''
        解析得到需要的代理列表数据
        :return: 
        '''
        # 从self.user_agent_list中随机取出一个字符串
        UA = random.choice(self.user_agent_list)
        print('随机产生的UA是====%s' % UA)
        headers = {
            'User-Agent': UA
        }
        response = requests.get(url=self.proxy_get_url, headers=headers, timeout=self.timeout)
        html = response.text
        # 获取<td></td>里面的所有内容
        list = re.findall(r'<td>(.*?)</td>', html)
        for index in range(int(len(list) / 6)):
            http = list[index * 6 + 3]
            ip = list[index * 6]
            port = list[index * 6 + 1]
            # 过滤掉一些socket连接
            if re.search(r'(HTTP|HTTPS)', http) is None:
                continue
            proxy = '%s://%s:%s' % (http, ip, port)
            self.proxy_list.append(proxy)
        print(self.proxy_list)

    def visit_url_by_proxy_1(self):
        self.get_proxy_list()
        for i in range(len(self.proxy_list)):
            self.visit_url_by_proxy(self.visit_url, self.timeout, self.proxy_list[i], )

    def visit_url_by_proxy(self, url, timeout, proxy=None, num_retries=6, sleep_time=2):
        UA = random.choice(self.user_agent_list)
        http = re.split(r'//', proxy)[0]
        proxies = {
            http: proxy,
        }
        print('随机产生的UA是====%s' % UA)
        headers = {
            'User-Agent': UA
        }
        if proxy == None:  # 没有使用代理的时候
            try:
                response = requests.get(url=url, headers=headers, timeout=timeout)
                status_code = response.status_code
                print('随机产生的代理是====%s,返回的状态码是===%d' % (proxies, status_code))
            except:
                if num_retries > 0:  ##num_retries是我们限定的重试次数
                    time.sleep(sleep_time)  ##延迟十秒
                    print('获取网页出错，10S后将获取倒数第：', num_retries, '次')
                    return self.visit_url_by_proxy(url, timeout, num_retries - 1)  ##调用自身 并将次数减1
                else:
                    print('开始使用代理')
                    time.sleep(sleep_time)
                    proxy = random.choice(self.proxy_list)
                    return self.visit_url_by_proxy(url, timeout, proxy, )  ##代理不为空的时候
        else:
            try:
                response = requests.get(url=url, headers=headers, proxies=proxies, timeout=timeout)
                status_code = response.status_code
                print('随机产生的代理是====%s,返回的状态码是===%d' % (proxies, status_code))
            except:
                if num_retries > 0:
                    time.sleep(sleep_time)
                    proxy = random.choice(self.proxy_list)
                    print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                    print(u'当前代理是：', proxy)
                    return self.visit_url_by_proxy(url, timeout, proxy, num_retries - 1)
                else:
                    print(u'代理也不好使了！取消代理')
                    return self.visit_url_by_proxy(url, timeout)


if __name__ == '__main__':
    proxy_handler = ProxyHandler()
    proxy_handler.visit_url_by_proxy_1()
