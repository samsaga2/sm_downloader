import os, sys
from os import path
from pyquery import PyQuery as pq
from ziputil import zipfolder, create_zip
from downloader import Downloader

ROOT_PATH = path.realpath(path.dirname(__file__))

class SubmangaPage(object):
    def __init__(self, base_url):
        self.base_url = base_url

        self.name = [p for p in base_url.split('/') if p!=''][-1]
        self.host = 'http://submanga.com'

        self.output_dir = ROOT_PATH + '/library/' + self.name
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.cbz_dir = ROOT_PATH + '/library/cbz/'
        if not os.path.exists(self.cbz_dir):
            os.makedirs(self.cbz_dir)

        self.download_all_chapters()

    def download_all_chapters(self):
        html_page = pq(self.base_url+'/completa')
        html_chapters = html_page('table.caps tr td.s a')
        url_chapters = [c.values()[-1] for c in html_chapters]
        self.make_directories_and_download(url_chapters)

    def make_directories_and_download(self, url_chapters):
        url_chapters.reverse()
        for index in range(len(url_chapters)):
            url = url_chapters[index]
            chap_id = url.split('/')[-1]
            chap_name = url.split('/')[-2]
            chap_dir = self.output_dir + '/' + chap_name
            if not os.path.exists(chap_dir):
                os.makedirs(chap_dir)
            print 'Chapter "%s" [%d/%d]' % (chap_name, index+1, len(url_chapters))
            self.process_page_and_download(chap_id, chap_dir)
            self.compress_chapter(chap_name)

    def process_page_and_download(self, page_id, page_dir):
        if os.path.exists(page_dir + '/.skip'):
            return

        page_url = self.host + '/c/' + page_id
        page_html = pq(page_url)

        #obtengo la url de descarga base
        page_base_url = page_html('body div a img')[0].values()[-1]
        temp_filename = page_base_url.split('/')[-1]
        url_down_base = page_base_url[:len(temp_filename)*-1]

        #descargo la imagen de cada capitulo
        cont = 0
        select = page_html('select option')
        downloader = Downloader()
        while len(select) > cont:
            for i in range(1, len(select)+1):
                url = url_down_base + str(i) + '.jpg'
                filename = page_dir + '/' + str(i).rjust(4,'0') + '.jpg'
                print '  downloading page [%i/%i]            \r' % (i, len(select)),
                sys.stdout.flush()
                downloader.start(url, filename)
                cont += 1
        downloader.wait()
        print ' '*40,'\r',

        #una vez descargado e folder con las imagenes crea un archivo .skip para
        # que no vuelva a descargar el capitulo
        file_skip = open(page_dir + '/.skip', 'w')
        file_skip.close()

    def compress_chapter(self, chapter_name):
        chap_dir = self.output_dir + '/' + chapter_name
        if chapter_name.isdigit():
            chapter_name = chapter_name.rjust(4,'0')
        filename = self.cbz_dir + self.name + '__' + chapter_name + '.cbz'
        if os.path.exists(chap_dir) and not os.path.exists(filename):
            print '  compressing\r',
            sys.stdout.flush()
            create_zip(chap_dir, '', filename )
            print ' '*40,'\r',
