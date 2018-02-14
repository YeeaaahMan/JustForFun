from __future__ import print_function #, unicode_literals
import os
import re
import sys

if sys.version_info < (3,0):
    import urllib2
    
else:
    import urllib.request as urllib2
    raw_input = input

# print(sys.version_info)

SITE_URL = "https://myzuka.club/"
# "https?:\/\/[w.]*myzuka.\w*\/"

def rplcr(text):
    ss = {"\\": " ",
          "/": " ",
          ":": " ",
          "*": " ",
          "?": "",
          '"': "'",
          "<": " ",
          ">": " ",
          '|': " ",
          "&#39;" : "'",
          "&amp;" : "&",
          '_myzuka.club': '',
          '_myzuka.org': '',
          '_myzuka.fm': '',
          '_myzuka.me': '',
          '_myzuka.mp3': '.mp3'
          }
    for k in ss:
        if k in text:
            text = text.replace(k, ss[k])
    return text

def Request(url):
    return urllib2.Request(
        url,
        data=None,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        ) 

def loader(link, file_name):
    req = Request(link) 
    
    f = urllib2.urlopen(req)
    data = f.read()
    with open(file_name, "wb") as code:
        code.write(data)
    
def download_song(song_url,
                  artist = u'',
                  year = u'',
                  album = u''):
    # The name of folder can't end on '.' in Windows =(
    # I use 'while' for cases when name ends on '...' 
    while artist[-1] == '.':
        artist = artist[:-1]
    while album[-1] == '.':
        album = album[:-1]

    # Deletion of symbols \ / " * ? < > |
    artist = rplcr(artist)
    album = rplcr(album)

    if not os.path.exists(artist):
        os.mkdir(artist)
    if not os.path.exists(artist+u'/'+year+u' - '+album):
        os.mkdir(artist+u'/'+year+u' - '+album)
        
    req = Request(song_url)  
    song_page = urllib2.urlopen( req ).read()
    # """itemprop="audio" href="/Song/Download/721913?t=635938335480692389&amp;s=de3221f231e2fe70603ba1a9124ba5d2"""
    download_url = SITE_URL + re.findall('''itemprop="audio" href="(\S*)"''', song_page.decode("utf-8"))[0]
    download_url = download_url.replace('&amp;', '&')

    req2 = Request(download_url) 
    song = urllib2.urlopen( req2 )

    byte_size = int( song.info()["Content-Length"])
    size = str( round( byte_size / (1024.**2), 2) )  + ' MB'
    name = re.findall("filename=(\S*)" , song.info()["content-disposition"])[0]
    # Replacement of bad symbols
    name = rplcr(name)

    name = name.replace( '_'+'_'.join(artist.lower().split(' ')),'')
    new_name = []
    for word in name.split('_'):
        new_name.append(word.capitalize())
    name = ' '.join(new_name)
    name = name[:2] +' -'+ name[2:]

    folder = artist + '/' + year + ' - ' + album + '/'
    print(name, ' --> ', size+':', end=' ')

    song_path = folder + name
    if not os.path.exists(song_path):
        print("loading", end=' ')
        loader(song.url, song_path)
        print("done.")
    elif os.path.exists( song_path ) and int(os.path.getsize(song_path)) < byte_size:
        print("loading", end=' ')
        loader(song.url, song_path)
        print("done.")
    else:
        print("already exists.")
        #print "Song already exists. Continue..."

def get_songs(album_url):
    req = Request(album_url)
    page = urllib2.urlopen( req ).read()
    
    songs = re.findall(u"""href="(\S*)" title='""", page.decode("utf-8"))
    print("\nGot " + str(len(songs)) + " songs!")
    for i in range(0, len(songs)):
        songs[i] = SITE_URL + songs[i]
        #print songs[i]
    return songs

def download_album(album_url):
    req = Request(album_url)
    album_page = urllib2.urlopen( req ).read()
    #print "album_page", len(album_page)
    #print album_page
    info = re.findall("<h1>(.*)</h1>" , album_page.decode("utf-8"))[0] # problem
    artist = re.findall('(.*) - ', info)[0]
    album = re.findall(' - (.*)\(\d\d\d\d\)', info)[0].strip()
    year = re.findall('\((\d\d\d\d)\)', info)[0]

    artist = artist.replace("&#39;", "'")
    artist = artist.replace("&amp;", "&")
    album = album.replace("&#39;", "'")
    album = album.replace("&amp;", "&")
    
    print(artist)
    print(year, u'-', album)
    
    songs = get_songs(album_url)
    for item in songs:
        download_song(item, artist, year, album)
    print('\n')

def find_albums(albums_url):
    req = Request(albums_url)
    albums_page = urllib2.urlopen( req ).read()
    albums = re.findall('data-type="2".*?<img', albums_page.decode("utf-8").replace('\n',''))[1:]
    print("Got", len(albums), "studio albums...\n")
    for i in range( len(albums)):
        albums[i] = SITE_URL + re.findall("""href="(\S*)"><img""", albums[i])[0]

    return albums

def download_artist(artist_url):
    if artist_url.endswith('/Albums'):
        albums_url = artist_url
    else:
        albums_url = artist_url + '/Albums'
    albums = find_albums(albums_url)

    i = 1
    for album_url in albums:
        print("[%s/%s]" % (i ,len(albums)), end=' ')
        download_album(album_url)
        i += 1

def chooser():
    choose = raw_input("Enter album or artist URL from myzuka.fm: ")
    SITE_URL = re.findall("https?:\/\/[w.]*myzuka.\w*\/", choose)[0]
    
    if "Album" in choose.split('/')[:4]:
        download_album(choose)
    else:
        download_artist(choose)

#download_album( raw_input('Enter album URL: ') )
#download_artist( raw_input('Enter artist URL: ') )
if __name__ == '__main__':
    #chooser()
    try:
        chooser()
    except KeyboardInterrupt:
        print("\n\nDownload canceled.")
    except Exception as e:
        print("\nAn error occurred. 8(\n" + e)
    raw_input("Press ENTER to quit.")

