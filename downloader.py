import threading
import os
from os import path
import urllib2

class Downloader():
    def __init__(self, max_threads=8):
        self.threads = []
        self.max_threads = max_threads

    def start(self, url, filename):
        t = threading.Thread(target=self.download, args=(url, filename))
        self.threads.append(t)
        t.start()

        if len(self.threads) >= self.max_threads:
            self.wait()

    def download(self, url, filename):
        if os.path.exists(filename):
            return

        file_photo = open(filename, 'w')
        try:
            resp = urllib2.urlopen(url, timeout=60)
            file_photo.write(resp.read())
            file_photo.close()
        except:
            file_photo.close()
            os.remove(filename)
            print 'error downloading', url

    def wait(self):
        for t in self.threads:
            while t.isAlive():
                t.join(1)
        self.threads = []
