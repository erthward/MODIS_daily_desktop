from datetime import date

# define filepaths
descrip_filepath = '/home/drew/MODIS_daily_img/today.txt'
img_filepath = '/home/drew/Pictures/MODIS_daily.jpg'
txt_filepath = '/home/drew/MODIS_daily_img/today.php'

# read in the last date with data downloaded
with open(descrip_filepath, 'r') as f:
    last_date = f.readlines()[0].strip()
    today = date.today().strftime('%d-%m-%Y')

# if newest download is not today, then ask whether to run the script
if last_date != today:
    decision = None
    invalid_response_msg = ''
    while decision not in ['y', 'n']:
        print(invalid_response_msg)
        decision = input(('\n\nThere is a new daily MODIS image. '
                          'Download it now? (y/n)'))
        decision = decision.lower()
        invalid_response_msg = ("\n\tI'm sorry. That was "
                                "an invalid response...\n")
    if decision == 'y':
        print('\n\n')
        import wget
        import string
        import re
        import os
        import textwrap
        import pydoc

        # print informative header
        header = '* DOWNLOADING DAILY MODIS DESKTOP IMAGE *'
        header = '*' * len(header) + '\n' + header + '\n' + '*' * len(header) + '\n'

        print(header)
        # get the image
        print('DOWNLOADING IMAGE...')
        img_today = date.today().strftime('%m%d%Y')
        url = ('http://modis.gsfc.nasa.gov/gallery/'
               'images/image%s_250m.jpg') % img_today
        try:
            img_file = wget.download(url)
        except Exception:
            try:
                url = re.sub('250m', '500m', url)
                img_file = wget.download(url)
            except Exception:
                url = re.sub('500m', '1km', url)
                img_file = wget.download(url)
        print(url)
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
        #wrap the text
        descrip = '\n'.join(textwrap.wrap(descrip, width=80))
        # add today's date to the text file
        descrip = today + '\n\n' + descrip
        # add the website link
        descrip = descrip + '\n\n' +  'URL:\n---\n' + txt_url + '\n\n'
        with open(descrip_filepath, 'w') as f:
            f.write(descrip)
        pydoc_header = '* DAILY MODIS DESKTOP IMAGE *'
        pydoc_header = ('*' * len(pydoc_header) + '\n' + pydoc_header 
                        + '\n' + '*' * len(pydoc_header) + '\n\n')
        pydoc_txt = pydoc_header + 'DESCRIPTION:\n-----------\n' + descrip
        pydoc.pager(pydoc_txt)
        # get rid of the PHP file
        os.remove(txt_filepath)
    else:
        print(('\n\n\tOkay. You will be prompted again in the next '
               'terminal window you open.\n\n'))
