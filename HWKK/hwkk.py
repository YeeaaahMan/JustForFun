import urllib, re
from BeautifulSoup import *
# import xml.etree.ElementTree as ET

def getVideoURL(link = 'http://kohana.stb.ua/episode/15-letnego-prestupnika-otpravili-na-perevospitanie-v-kadetskoe-uchilishhe-chast-1-iz-4-sezon-6-vypusk-11-ot-22-12-2015/'):
    page = urllib.urlopen(link)
    Page = page.read()
    page.close()
    
    video = re.findall('"(\S*mediafile\S*)"', Page)[0].replace('_imgx400.jpg', '.mp4')
    return video

def getPagesURLs(link='http://kohana.stb.ua/episode/15-letnego-prestupnika-otpravili-na-perevospitanie-v-kadetskoe-uchilishhe-chast-1-iz-4-sezon-6-vypusk-11-ot-22-12-2015/'):
    Pages = list()
    
    page = urllib.urlopen(link)
    P = page.read()
    soup = BeautifulSoup(P)
    page.close()

    tags = soup('div')
    for tag in tags:
        if tag.get('class', None) == 'entry-content styling':
            return re.findall('href="(\S*)"', str(tag))

link = raw_input("Enter kohana.stb.ua link: ")
print
print getVideoURL(link)

for page in getPagesURLs(link):
    print getVideoURL(page)

raw_input("Done! Press ENTER... ")
