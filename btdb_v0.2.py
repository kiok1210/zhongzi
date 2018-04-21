# -*- coding: UTF-8 -*-
from soup_tool import Soup
from soup_tool import MyThread
from time import sleep, ctime

'''
使用关键词输入抓取磁力链接
目标网站：btdb
依赖工具类：soup_tool
version:0.1 
version:0.2 1、按照title去重；2、单位不是GB的种子不再获取
author:yaowei
date:2018-04-12
'''


class Capture:

    def __init__(self):
        self.index_page_url = 'http://btdb.to/'
        self.one_page_url = 'http://btdb.to/q/:key'
        self.list_page_url = 'http://btdb.to/q/:key/?'
        self.folder_path = 'btdb/'
        # 每个线程的沉睡时间
        self.sleep_time = 2
        # 缓存番号
        self.cache_fh = []
        # 缓存种子
        self.cache_zz = []
        # 缓存种子中的视频名称
        self.cache_dn = []
        # 文件路径
        self.file_path = ''

    def readPageFromSearch(self, search_key):
        """
        根据输入key读取搜索页面
        :param search_key:
        :return:
        """

        # 创建文件夹 /magnet/search_key
        path = self.folder_path + search_key
        Soup.create_folder(path)
        self.file_path = path

        # 打开搜索页面第1页
        page_url = self.one_page_url.replace(':key', search_key)
        print(page_url)
        soup_html = Soup.get_soup(page_url)
        try:
            list_a = soup_html.find("ul", {'class': 'pagination'}).find_all('a')
            last_a = list_a[len(list_a) - 2]
            last = last_a.get('href')
            # last = last_str.split('/')[-1]
            # last = last_arr[last_arr.length() - 1]
            item_size = int(last)
        except BaseException as msg:
            item_size = 1
            print('count error', msg)

        print('item_size=====', item_size)
        if item_size == 1:
            # 只有一条不再重复读取
            self.readPageFromSoup(soup_html)
        else:

            list_page_url = self.list_page_url.replace(':key', search_key)
            self.readPageByThread(item_size, path, list_page_url)

    # 多线程读取，每个分页都是一个线程
    def readPageByThread(self, item_size, path, list_page_url):

        threads = []
        # 循环打开分页链接，读取分页页面
        for item in range(item_size):
            page = str(item + 1)
            new_page_url = list_page_url.replace("?", page)
            new_path = path + '/' + page + '.txt'
            print(new_path, '---', new_page_url)

            t = MyThread(self.readPagetoTxt, (new_page_url, new_path, self.sleep_time), self.readPagetoTxt.__name__)
            # t = threading.Thread(target=self.testRun, args=( str(i) ))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print('all end', ctime())

    # 读取单章内容并写入
    def readPagetoTxt(self, page_url, path, _time):

        # 先等待
        sleep(_time)

        soup_html = Soup.get_soup(page_url)

        self.readPageFromSoup(soup_html)
        # self.cache_write()  # 前置 self.readPageFromSoup(soup_html, path)

    # 读取单页内容上的magnet
    def readPageFromSoup(self, soup_html):

        # new_path = Soup.purge_file(path)  # 返回合法文件名

        # 读取所有链接
        list_a = soup_html.find_all('a', {'title': 'Download using magnet'})

        content = ''

        for a in list_a:
            href = a.get('href')  # magnet

            title = a.parent.parent.find('h2', {'class': 'item-title'}).find('a').get('title')

            # 只取1GB以上的片源
            next_node = a.find_next_sibling()
            size = next_node.text
            if 'GB' not in size:
                continue

            title = title.upper()
            if title in self.cache_fh:
                continue

            self.cache_fh.append(title)

            dn = href.split('&')[1].split('.')[0].upper()
            if dn in self.cache_zz:
                continue

            content = content + href + '\n'

            self.cache_dn.append(dn)
            self.cache_zz.append(href)
            # self.cache_zz.append({'title': title, 'size': size, 'magnet': href})

        # print(new_path, len(self.cache_zz), self.cache_zz)
        # Soup.write_file(new_path, content)  # 写入文件 v0.1 使用

    # 每10条写入
    def cache_write(self):
        zz_len = len(self.cache_zz)
        page = 0
        content = ''
        print('zz_len', zz_len)
        print(self.cache_fh)

        for i in range(1, zz_len):
            content = content + self.cache_zz[i] + '\n'

            if i % 10 == 0 \
                    or (zz_len < 10 and i is zz_len - 1):
                page = page + 1
                new_path = self.file_path + '/' + str(page) + '.txt'
                # 写入文件 v0.1 使用
                print(new_path, content)
                Soup.write_file(new_path, content)
                content = ''

    def run(self):
        try:
            self.readPageFromSearch('栄川乃亜')

            # 线程采集完后写入数据
            self.cache_write()
        except BaseException as msg:
            print(msg)


Capture().run()
