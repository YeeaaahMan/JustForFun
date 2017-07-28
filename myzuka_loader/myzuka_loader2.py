import re
import urllib2
import os

# TODO: &#39; -> '

def loader(link, file_name):
    req = urllib2.Request(
        link, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    )  
    
    f = urllib2.urlopen(req)
    data = f.read()
    with open(file_name, "wb") as code:
        code.write(data)
    
def download_song(song_url,
                  artist = u'',
                  year = u'',
                  album = u''):
    # The name of folder can't end on '.' in Windows =(
    while artist[-1] == u'.':
        artist = artist[:-1]
    while album[-1] == u'.':
        album = album[:-1]

    # Exception for AC/DC
    artist = artist.replace("/", " ")
    artist = artist.replace("&#39;", "'")
    album = album.replace("/", " ")
    album = album.replace("&#39;", "'")
    

    if not os.path.exists(artist):
        os.mkdir(artist)
    if not os.path.exists(artist+u'/'+year+u' - '+album):
        os.mkdir(artist+u'/'+year+u' - '+album)
        
    req = urllib2.Request(
        song_url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    )  
    song_page = urllib2.urlopen( req ).read()
    # """itemprop="audio" href="/Song/Download/721913?t=635938335480692389&amp;s=de3221f231e2fe70603ba1a9124ba5d2"""
    download_url = "https://myzuka.fm" + re.findall('''itemprop="audio" href="(\S*)"''', song_page)[0]
    download_url = download_url.replace('&amp;', '&')

    req2 = urllib2.Request(
        download_url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    ) 
    song = urllib2.urlopen( req2 )

    byte_size = int( song.info()["Content-Length"])
    size = str( round( byte_size / (1024.**2), 2) )  + ' MB'
    name = re.findall("filename=(\S*)" , song.info()["content-disposition"])[0]
    name = name.replace('_myzuka.org', '')
    name = name.replace('_myzuka.fm', '')

    name = name.replace( '_'+'_'.join(artist.lower().split(' ')),'', 1)# fix for case when song name and artist name are same.
    new_name = []
    for word in name.split('_'):
        new_name.append(word.capitalize())
    name = ' '.join(new_name)
    name = name[:2] +' -'+ name[2:]

    folder = artist + '/' + year + ' - ' + album + '/'
    print name, '  --> ', size+':', 

    song_path = folder + name
    if not os.path.exists(song_path):
        print "loading",
        loader(song.url, song_path)
        print "done."
    elif os.path.exists( song_path ) and int(os.path.getsize(song_path)) < byte_size:
        print "loading",
        loader(song.url, song_path)
        print "done."
    else:
        print "already exists."
        #print "Song already exists. Continue..."

def get_songs(album_url):
    req = urllib2.Request(
        album_url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    )    
    page = urllib2.urlopen( req ).read()
    
    songs = re.findall(u"""href="(\S*)" title='""", page)
    print "\nGot " + str(len(songs)) + " songs!"
    for i in range(0, len(songs)):
        songs[i] = "https://myzuka.fm" + songs[i]
        #print songs[i]
    return songs

def download_album(album_url):
    req = urllib2.Request(
        album_url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    )
    album_page = urllib2.urlopen( req ).read()
    #print "album_page", len(album_page)
    #print album_page
    info = re.findall("<h1>(.*)</h1>" , album_page)[0] # problem
    artist = re.findall('(.*) - ', info)[0].decode('utf-8')
    album = re.findall(' - (.*)\(\d\d\d\d\)', info)[0].strip().decode('utf-8')
    year = re.findall('\((\d*)\)', info)[0].decode('utf-8')
    print artist
    print year, u'-', album
    
    songs = get_songs(album_url)
    for item in songs:
        download_song(item, artist, year, album)
    print '\n'

def find_albums(albums_url):
    req = urllib2.Request(
        albums_url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
    )
    albums_page = urllib2.urlopen( req ).read()
    albums = re.findall('data-type="2".*?<img', albums_page.replace('\n',''))[1:]
    print "Got", len(albums), "studio albums...\n"
    for i in range( len(albums)):
        albums[i] = "https://myzuka.fm" + re.findall("""href="(\S*)"><img""", albums[i])[0]

    return albums

def download_artist(artist_url):
    if artist_url.endswith('/Albums'):
        albums_url = artist_url
    else:
        albums_url = artist_url + '/Albums'
    albums = find_albums(albums_url)

    i = 1
    for album_url in albums:
        print "[%s/%s]" % (i ,len(albums)), 
        download_album(album_url)
        i += 1

def chooser():
    choose = raw_input("Enter album or artist URL from myzuka.fm: ")
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
        print "\n\nDownload canceled."
    except :
        print "\nAn error occurred. 8(\n"
    raw_input("Press ENTER to quit.")
