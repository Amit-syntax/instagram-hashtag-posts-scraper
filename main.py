import re
import pandas as pd
import argparse
import os
import time
import wget
import pathlib as pth

from instaclient.errors import *
from instaclient import InstaClient


parser = argparse.ArgumentParser()
parser.add_argument('--hashtag=',
                    type=str,
                    help='get posts of instagram hashtag')
parser.add_argument('--postcount=',
                    type=str,
                    help='how much post you want to scrape')
parser.add_argument('--o=',
                    type=str,
                    help='output csv file name or default file name "output.csv"')
parser.add_argument('--scraperemaining',
                    action='store_true',
                    help='scrape remaining post url form "post_url.txt"')
parser.add_argument('--ImagesPath=',
                    type=str,
                    help='give images folder path or it will take default path as "Images"')

args = vars(parser.parse_args())
print(args)

if (not(args["hashtag="]) and not(args["scraperemaining"])):
    parser.print_help()
    exit()

cred = open("credentials.txt", "r")
exec(cred.read())
cred.close()
hashtag = args["hashtag="]
images_path = args["ImagesPath="] if args["ImagesPath="] else "Images"
postcount = int(args["postcount="]) if args["postcount="] else None
ouputfile = "output.csv" if (args["o="] == None) else args["o="]
scrapeRemaining = args["scraperemaining"]

global client
client = InstaClient(driver_path='chromedriver.exe')

global df

df = pd.DataFrame({"likes": [], "comments": [], "location": [],
                   "source_url": [], "post_url": [], "hashtags": []})
df["likes"] = df["likes"].astype(int)
df["comments"] = df["comments"].astype(int)


def getHashtags(caption):

    return "#".join(re.findall(r"#(\w+)", caption))


def getCommentsCount(surl):
    global client
    client.driver.get("https://www.instagram.com/p/"+surl)
    time.sleep(2)
    a = client.driver.find_element_by_class_name('r8ZrO')
    return a.find_element_by_tag_name("span").text


def scrapePosts(posts):
    global df
    for count, post in enumerate(posts):
        try:
            print("\n", count+1, " no of posts scraped out of ", len(posts))

            post = client.get_post(post)
            download_img = False
            extintions = [".png", ".jpg", ".gif"]
            series = pd.Series({
                "likes": int(post.likes_count) if post.likes_count else 0,
                "comments": len(post.comments) if len(post.comments) < 20 else getCommentsCount(posts[count]),
                "location": str(post.location.address).replace("Address", "").replace("<", "").replace(">", "") if post.location else "",
                "post_url": str('https://www.instagram.com/p/')+posts[count],
                "source_url": post.media[0].src_url if post.media else "",
                "hashtags": getHashtags(post.caption),
                "owner": post.get_owner().username
            })

            for ext in extintions:
                if ext in series["source_url"]:
                    download_img = True
                    break

            if series["source_url"] and download_img:
                if images_path:
                    path = str(pth.Path(images_path) /
                               pth.Path(post.shortcode+ext))
                    if not(os.path.exists(str(pth.Path(images_path)))):
                        os.mkdir(str(pth.Path(images_path)))
                    wget.download(series["source_url"], path)
            df = df.append(
                series,
                ignore_index=True
            )
        except KeyboardInterrupt:
            a = df.copy()
            a.to_csv(ouputfile, index=False)
            exit()

        # except:
        #     print("-------------- error in scraping 1 post -------------------")
        #     a = df.copy()
        #     a.to_csv(ouputfile, index=False)

        finally:
            a = open("post_url.txt", "w")
            a.write("\n".join(posts[count:]))
            a.close()

            if count % 15 == 0:
                a = df.copy()
                a.to_csv(ouputfile, index=False)


client.login(username=username, password=password)
posts = []
if scrapeRemaining:
    if os.path.exists("post_url.txt") and scrapeRemaining:
        fl = open("post_url.txt", "r")
        posts.extend(fl.read().split("\n"))
        print(posts[:10])
        fl.close()
    else:
        print("'post_url.txt' does not exists try to scrape with hashtah")
        exit()

if hashtag:
    hashtag = client.get_hashtag(tag=hashtag)

    if postcount == None:
        posts = hashtag.get_posts()
    else:
        posts = hashtag.get_posts(count=postcount)

    print(
        "\n\n\n\n\t---------------IT GOT {0} LINKS---------------".format(len(posts)))

    print("\n\n\n--------------- NOW STARTING TO SCRAPE DATA ---------------")


posts = list(dict.fromkeys(posts).keys())

a = open("post_url.txt", "w")
a.write("\n".join(posts))
a.close()

scrapePosts(posts)
df.to_csv(ouputfile, index=False)
