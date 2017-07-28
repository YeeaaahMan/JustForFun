import urllib, re, time

def getVideoURL(link):
    """ Function get page's link and return 'video part's direct link. """
    page = urllib.urlopen(link)
    Page = page.read()
    page.close()
    
    video = re.findall('"(\S*mediafile\S*)"', Page)[0].replace('_imgx400.jpg', '.mp4')
    return video

def getPagesURLs(link):
    """ Function finds links to pages with another episode's parts and returns list of pages. """
    P = urllib.urlopen(link).read()
    from_ = P.find('entry-content styling')
    _to = P[from_:].find('</div>')
 
    return [link] + re.findall('href="(\S*)"', P[ from_ : from_+_to ])

def getURLs(pages):
    """Function gets list of pages with episode's parts and returns tuple, that contains list of video's direct links and link to part from previos episode."""
    result = list()
    
    for p in pages[:-1]:
        try:
            p = getVideoURL(p)
        except:
            continue
        if p not in result:
            result.append(p)
    return (result, pages[-1])


link = raw_input("Enter kohana.stb.ua link: ")
filename = 'hwkk_' + time.strftime("%y.%m.%d_%H:%M", time.localtime()) + '_.txt'
fh = open(filename, 'w')

while True:
    URLs = getURLs( getPagesURLs(link) )
    fh.write('\n' + ' '.join(link.split('/')[-2:]) + '\n')

    print "\nFiles URLs:"
    for l in URLs[0]:
        print l
        fh.write(l + '\n')
    print "\nPrevious episode:\n", URLs[1]

    chose = raw_input("\n[Press ENTER to continue or enter 'STOP' to exit]\n")
    if chose.lower() == 'stop':
        break
    else:
        link = URLs[1]
fh.close()
