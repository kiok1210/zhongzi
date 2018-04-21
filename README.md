# zhongzi
使用关键词输入抓取磁力链接

### btdb.to

    def run(self):
        try:
            self.readPageFromSearch('栄川乃亜')

            # 线程采集完后写入数据
            self.cache_write()
        except BaseException as msg:
            print(msg)
            
 ### zhongziso
     def run(self):
        try:
            self.readPageFromSearch('KIRAY-049')
        except BaseException as msg:
            print(msg)