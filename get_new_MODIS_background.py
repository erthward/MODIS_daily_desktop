from datetime import date

show_txt = False
use_pywal = True
pywal_theme_type = 'light'
pywal_bgrounds = {'light': "#f5f5ed",
                  'dark': "#545350"
                 }


# define filepaths
descrip_filepath = '/home/deth/MODIS_daily_img/today.txt'
img_filepath = '/home/deth/Pictures/MODIS_daily.jpg'
txt_filepath = '/home/deth/MODIS_daily_img/today.php'

# read in the last date with data downloaded
with open(descrip_filepath, 'r') as f:
    last_date = f.readlines()[0].strip()
    today = date.today()
    # subtract a day to account for fact that US is behind Australia
    # and so the text doesn't get released until after the workday here
    today = date.fromordinal(today.toordinal()-1).strftime('%d-%m-%Y')

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
        # try to grab a scrollover URL if there is one
        scrollover_url_patt='(?<=<a href=").*go\.nasa\.gov.*(?=">here</a>)'
        scrollover_url = re.search(scrollover_url_patt, descrip)
        if scrollover_url is not None:
            scrollover_url = scrollover_url.group()
        # format the description text more
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
        # add the scrollover link at the bottom, if found
        if scrollover_url is not None:
            descrip = descrip + ('\n' +  'SCROLLOVER URL:\n---\n' +
                                 scrollover_url + '\n\n')
        with open(descrip_filepath, 'w') as f:
            f.write(descrip)
        pydoc_header = '* DAILY MODIS DESKTOP IMAGE *'
        pydoc_header = ('*' * len(pydoc_header) + '\n' + pydoc_header
                        + '\n' + '*' * len(pydoc_header) + '\n\n')
        pydoc_txt = pydoc_header + 'DESCRIPTION:\n-----------\n' + descrip
        # show text, if required
        if show_txt:
            pydoc.pager(pydoc_txt)
        # get rid of the PHP file
        os.remove(txt_filepath)
        # use pywal to set the terminal colorscheme based on the new image
        if use_pywal:
            # get rid of the previous pywal colorscheme
            os.system('wal -c')
            # then create the new one
            cmd = ('wal --saturate 0.3 -i ./Pictures/MODIS_daily.jpg '
                   #'--backend colorz -%s -b "%s"') % (pywal_theme_type[0],
                   '--backend haishoku -%s -b "%s"') % (pywal_theme_type[0],
                                            pywal_bgrounds[pywal_theme_type])
            os.system(cmd)
    else:
        print(('\n\n\tOkay. You will be prompted again in the next '
               'terminal window you open.\n\n'))
