#!/usr/bin/env python
from submanga import SubmangaPage
import sys

if len(sys.argv) > 1:
    links = sys.argv[1:]
else:
    links = [raw_input('ingrese la direccion del manga ej: http://submanga.com/Nisekoi: ')]

for link in links:
    print
    print "===", link, "==="
    engine = SubmangaPage(link)
