# -*- coding: UTF-8 -*-
from soup_tool import Soup
from soup_tool import MyThread
from time import sleep, ctime

'''
使用关键词输入抓取磁力链接
依赖工具类 soup_tool
version:0.1 
author:yaowei
date:2018-04-12
'''


class Capture:

    def __init__(self):
        self.index_page_url = 'https://m.zhongzidi.com/'
        self.one_page_url = 'https://m.zhongzidi.com/list/?/1'
        self.list_page_url = 'https://m.zhongzidi.com/list/:key/?'
        self.folder_path = 'magnet/'
        # 每个线程的沉睡时间
        self.sleep_time = 2

    def readPageFromSearch(self, search_key):
        """
        根据输入key读取搜索页面
        :param search_key:
        :return:
        """

        # 创建文件夹 /magnet/search_key
        path = self.folder_path + search_key
        Soup.create_folder(path)

        # 打开搜索页面第1页
        page_url = self.one_page_url.replace('?', search_key)
        print(page_url)
        soup_html = Soup.get_soup(page_url)
        try:
            last_a = soup_html.find("a", text='尾页')
            last_str = last_a.get('href')
            last = last_str.split('/')[-1] # 读取从右往左第一个分割数据
            # last = last_arr[last_arr.length() - 1]
            item_size = int(last)
        except BaseException as msg:
            print('page error ',soup_html)
            item_size = 1

        print('item_size=====', item_size)
        if item_size == 1:
            self.readPageFromSoup(soup_html, path + '/' + '1.txt')
        else:

            list_page_url = self.list_page_url.replace(':key', search_key)
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

        self.readPageFromSoup(soup_html, path)

    @staticmethod
    def readPageFromSoup(soup_html, path):

        new_path = Soup.purge_file(path)  # 返回合法文件名

        # 读取所有链接
        list_a = soup_html.find_all('a', {'title': '磁力链接下载'})

        content = ''

        for a in list_a:
            href = a.get('href')  # magnet
            content = content + href + '\n'

        print('new_path', new_path, 'content', content)
        Soup.write_file(new_path, content)  # 写入文件

    def run(self):
        try:
            self.readPageFromSearch('KIRAY-049')
        except BaseException as msg:
            print(msg)


Capture().run()
