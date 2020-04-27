import wget
from datetime import date
import string
import re
import os

# desktop image file
filepath = '/home/drew/Pictures/MODIS_daily.jpg'

# get the image
today = date.today().strftime('%m%d%Y')
url = 'http://modis.gsfc.nasa.gov/gallery/images/image%s_500m.jpg' % today
img_file = wget.download(url)
os.replace(img_file, filepath)

# get the descriptive text
text_today = date.today().strftime('%Y-%m-%d')
text_url = ('http://modis.gsfc.nasa.gov/gallery/'
            'individual.php?db_date=%s') % text_today
text_file = '../today.php'
php_file = wget.download(text_url, out=text_file)
with open(php_file, 'r') as f:
    text = f.read()
descrip = text.split('<b>Image Facts')[0].split('Share')[-1]
for ws in string.whitespace[1:]:
    descrip = re.sub(ws, '', descrip)
tags = re.compile('<.*?>')
descrip = re.sub(tags, '', descrip).strip()
with open('../today.txt', 'w') as f:
    f.write(descrip)


