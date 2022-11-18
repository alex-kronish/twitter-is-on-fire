#!/usr/bin/python3

import requests
import json
import time
from datetime import datetime
import os
from urllib.parse import urlparse


def scrape_time(input_file,output_path):
    source=open(input_file,'rt+')
    dataset=json.load(source)
    source.close()
    cleaned_links_list=[]
    for d in dataset:
        #tweet_txt=d["tweet"]["full_text"]
        #tweet_id=d["tweet"]["id"]
        #favs=d["tweet"]["favorite_count"]
        #rts=d["tweet"]["retweet_count"]
        #reply_to_id=d["tweet"].get("in_reply_to_status_id",'-1')
        #post_date_unparsed_str=d["tweet"]["created_at"]
        #Sat Nov 05 17:35:36 +0000 2022
        #post_date_fmt="%a %b %d %H:%M:%S %z %Y"
        #post_date_parsed=datetime.strptime(post_date_unparsed_str,post_date_fmt)
        #post_date_reformatted=datetime.strftime(post_date_parsed,"%Y-%m-%d %H:%M:%S")
        media_exists_flag=False
        media_urls=[None,None,None,None]
        if d["tweet"]["entities"].get("media"):
            media_exists_flag=True
            media=d["tweet"]["extended_entities"]["media"]
            media_size=len(media)
            if d["tweet"]["extended_entities"]["media"][0].get("video_info"):
                videos_list=d["tweet"]["extended_entities"]["media"][0]["video_info"]["variants"]
                new_videos_list=[]
                for v in videos_list:
                    if v.get("bitrate"):
                        new_videos_list.append({"url":v["url"],"bitrate":int(v["bitrate"])})
                #print(str(new_videos_list))
                best_vid=max(new_videos_list,key=lambda x:x["bitrate"])
                cleaned_links_list.append(best_vid["url"])
                #print(media_urls[0])
            else: 
                for m in media:
                    cleaned_links_list.append(m["media_url_https"])

    print(cleaned_links_list)
    for l in cleaned_links_list:
        urlparsed=urlparse(l)
        #print(urlparsed)
        timestamp=datetime.now().strftime('%Y-%m-%d_%H-%M-%S_')
        filename=output_path+'/'+timestamp+os.path.basename(urlparse(l).path)
        req=requests.get(l)
        status=req.status_code
        if status==200:
            datachunk=req.content
            f=open(filename,'wb+')
            f.write(datachunk)
            f.close()
            print("Wrote file: "+filename)
        else:
            print("Uh oh! Response code wasn't 200? got "+str(status))
        time.sleep(2)
        



if __name__=='__main__':
    #bada bing
    #if you wanna use a windows path you have to double slash it like C:\\Users\\Alex\\TwitterScraperResults"
    input_file='/bots/twitter-archive-to-database-script/data/input/tweets.js'
    output_path='/bots/twitter-archive-to-database-script/data/output/'
    scrape_time(input_file,output_path)
    print("done")
