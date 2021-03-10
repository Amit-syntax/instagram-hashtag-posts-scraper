# instagram-hashtag-posts-scraper


```
usage: main.py [-h] [--hashtag= HASHTAG=] [[optional]--postcount= POSTCOUNT=] [--o= O=]
               [[optional]--scraperemaining] [[optional]--ImagesPath= IMAGESPATH=]

optional arguments:
  -h, --help            show this help message and exit.
  --hashtag=            get posts of instagram hashtag.
  --postcount=          how much post you want to scrape (if not given then it will scrape max posts it can scrape).
  --o=                  output csv file name or default file name "output.csv".
  --scraperemaining     scrape remaining post url form "post_url.txt".
  --ImagesPath=         give images folder path or it will take default path as "Images".
```

# setup the instagram-scraper
```
$ git clone https://github.com/Amit-syntax/insta-v2
$ cd insta-v2
$ python3 -m venv env
$ source env/bin/activate
$ cp instaclient/ -r ./env/lib/python3.8/site-packages
```

# requirements to install

```
pip install wget
pip install pandas
pip install selenium
pip install requests
```
boom you are ready to go.
