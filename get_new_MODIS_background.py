from datetime import date

# define filepaths
descrip_filepath = '/home/drew/MODIS_daily_img/today.txt'
img_filepath = '/home/drew/Pictures/MODIS_daily.jpg'
txt_filepath = '/home/drew/MODIS_daily_img/today.php'

# read in the last date with data downloaded
with open(descrip_filepath, 'r') as f:
    last_date = f.readlines()[0].strip()
    today = date.today().strftime('%d-%m-%Y')

# if newest download is not today then run the script
if last_date != today:
    import wget
    import string
    import re
    import os

    # print informative header
    header = '* DOWNLOADING DAILY MODIS DESKTOP IMAGE *'
    header = '*' * len(header) + '\n' + header + '\n' + '*' * len(header) + '\n'

    print(header)
    # get the image
    print('DOWNLOADING IMAGE...')
    img_today = date.today().strftime('%m%d%Y')
    url = ('http://modis.gsfc.nasa.gov/gallery/'
           'images/image%s_250m.jpg') % img_today
    print(url)
    img_file = wget.download(url)
    os.replace(img_file, img_filepath)
    
    # get the descriptive text
    txt_today = date.today().strftime('%Y-%m-%d')
    txt_url = ('http://modis.gsfc.nasa.gov/gallery/'
                'individual.php?db_date=%s') % txt_today
    print("\n\nDOWNLOADING TEXT...")
    php_file = wget.download(txt_url, out=txt_filepath)
    with open(php_file, 'r') as f:
        text = f.read()
    descrip = text.split('<b>Image Facts')[0].split('Share')[-1]
    for ws in string.whitespace[1:]:
        descrip = re.sub(ws, '', descrip)
    tags = re.compile('<.*?>')
    descrip = re.sub(tags, '', descrip).strip()
    # add today's date to the text file
    descrip = today + '\n\n' + descrip
    with open(descrip_filepath, 'w') as f:
        f.write(descrip)
    print('\n' * 2 + 'DESCRIPTION:\n-----------')
    print(descrip)
    # get rid of the PHP file
    os.remove(txt_filepath)
