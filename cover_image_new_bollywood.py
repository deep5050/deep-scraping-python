# download latest bollywood movie's cover image automatically (webmusic.cc) 
# it also creats new folders for each movie

# github/deep5050

from bs4 import BeautifulSoup as soup
import re
from urllib.request import urlopen
import os
import requests
import progressbar
import subprocess


def get_cover_image_url(url):
  html = urlopen(url)
  #http://37.webmusic.pw/music/hindi/movies/2017/r/rukh/img.jpg
  cover_expr = r'http://\d+\.webmusic\.\D+/music/hindi/movies/\d{4}/?.*/[\w.]+/img\.jpg'
  temp_buff = re.findall(cover_expr, str(html.read()))

  return str(temp_buff[0])

def download_file(url,file_name):
  r = requests.get(url, stream=True)
  f = open(img_name , 'wb')
  file_size = int(r.headers['Content-Length'])
  chunk = 1
  num_bars = file_size / chunk
  bar = progressbar.ProgressBar(max_value=num_bars).start()
  i = 0
  for chunk in r.iter_content():
    f.write(chunk)
    bar.update(i)
    i+=1
  f.close()
  return

 


# <a href="http://webmusic.cc/hindi_music.php?id=5012">Hate Story IV</a>
# expression for movie names
expr = re.compile(
    r'(http://webmusic.cc/hindi_music.php\?id=\d+)">([\w\s.]+)</a>')

#home page for the latest bollywood entries
url = 'http://webmusic.cc/music/mobile/hindi/latest.php'

response = urlopen(url)
bs_obj = soup(response.read(), "html.parser")
data = str(bs_obj)
response.close

#get the current directory and then create a new folder names 'latest-bollywood'
new_path = os.path.dirname(os.path.realpath(__file__))+'\latest-bollywood'

if not os.path.exists(new_path):
  os.makedirs(new_path)

subprocess.Popen('explorer ".\latest-bollywood"')

result = re.findall(expr, data)
#print(len(result)," results found :---->")

print("TOTAL",len(result)," files to download")
file_count = 1
for row in result:
  # row[0] is url and row[1] is the movie name
  # create a new folder for each movie name under the 'latest-bollyeood'
  temp_dir = new_path + '\\' + row[1]
  #print(temp_dir)

# create a folder if not exists
  if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

   # calling the function to get the cover image for the movie
  img_url = get_cover_image_url(row[0])
  # now download the image in that directory
  img_name = temp_dir + '\\' + row[1] + '.jpg'
  print(file_count," | DOWNLOADING ... ",img_url,"\n")
  download_file(img_url, img_name)

print("DOWNLOAD COMPLETE ")

#open the folder in explorer
subprocess.Popen('explorer new_path')
  
