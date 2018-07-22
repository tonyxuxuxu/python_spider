from bs4 import BeautifulSoup
import requests
import sys


class book_downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com'
        self.target = 'http://www.biqukan.com/0_790/'
        self.names = []
        self.urls = []

    def get_download_url(self):
        req = requests.get(url=self.target)
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[16:])
        for each in a[16:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_contents(self, target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0'*8, '\n\n')
        return texts

    def writer(self, name, path, text):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == '__main__':
    dl = book_downloader()
    dl.get_download_url()
    print('Start to download:')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '元尊.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  already downloaded:%.3f%%" % float(i/dl.nums*100) + '\r')
        sys.stdout.flush()

