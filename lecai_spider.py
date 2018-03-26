#coding:UTF-8
import os, re, lxml, json, requests
import config.cfg 
from lib.Logger import *
from bs4 import BeautifulSoup

# 抓取乐彩网
# 起始URL
json_config = "./config/lecai.json"
f = open(json_config, 'r', encoding='utf-8')
config_dict = json.load(f)
site_name = config_dict['site_name']

html = requests.get(config_dict['url_ex'])

soup = BeautifulSoup(html.content, "html.parser", from_encoding='utf-8')
tag_str = config_dict['pattern_tag_ex']['tag']
if 'class' in config_dict['pattern_tag_ex']:
    class_str = re.compile(config_dict['pattern_tag_ex']['class'])
    tags = soup.find_all(tag_str, class_=class_str)
else:
    tags = soup.find_all(tag_str)

# generate pre-defined auther list
ignore_auther_list = config_dict['ignore_auther_list']
auther_list = []
for link in config_dict['links']:
    auther_list.append(link['auther'])

CURRENT_INDEX = str(config.cfg.CURRENT_INDEX)

for tag in tags:
    try:
        inner_url = tag.a['href']  # 取得内部链接
    except KeyError:
        continue
    except TypeError:
        continue
    auther_and_index = tag.a.get_text()  # 取得作者名和期数

    inner_url_abs = config_dict['url_prefix'] + inner_url
    
    auther = ""
    index = ""
    index_pattern = config_dict['index_pattern']
    auther_pattern = config_dict['auther_pattern']
    if re.search(index_pattern, auther_and_index):
        index = re.search(index_pattern, auther_and_index).group(0)  # 期数
    else:
        pass
    if re.search(auther_pattern, auther_and_index):
        # Most case : auther + mark + index
        if site_name == "sina":
            auther = re.search(auther_pattern, auther_and_index).group(0)[:-3] #作者
        elif site_name == "zhcw":
            auther = re.search(auther_pattern, auther_and_index).group(1) #作者
        else:
            pass
        ### special case : auther + index + mark
        if re.findall(r'(^.*)(第?\d{5}期?)', auther) != []:
            auther = re.findall(r'(^.*)(第?\d{5}期?)', auther)[0][0]
    else:
        pass
    if auther == "" or index != CURRENT_INDEX:
        continue
    try:
        auther_id = auther_list.index(auther)
    except ValueError:
        if auther not in ignore_auther_list and index == CURRENT_INDEX:
            Logger.warn("Undefined auther :" + auther + "index:" + index)
        continue
 
    html_inner = requests.get(inner_url_abs)
    soup_inner = BeautifulSoup(html_inner.content, "html.parser", from_encoding='utf-8')
    tags_inner = soup_inner.find_all(config_dict['pattern_tag_in'])
    red_patterns = config_dict['links'][auther_id]['red_patterns']
    blue_patterns = config_dict['links'][auther_id]['blue_patterns']

    Logger.info( index + " : " + auther + " : " + inner_url_abs)
    for red_pattern in red_patterns:    
        extract_data_from_tag_int(tags_inner, red_pattern)
    for blue_pattern in blue_patterns:
        extract_data_from_tag_int(tags_inner, blue_pattern)
    if 'red_blue_patterns' in config_dict['links'][auther_id]:
        red_blue_patterns = config_dict['links'][auther_id]['red_blue_patterns']
        for red_blue_pattern in red_blue_patterns:
            extract_data_from_tag_int(tags_inner, red_blue_pattern, split = "+")

Logger.ok("All done!")

def extract_data_from_tag_int(tags_inner, pattern, split = None):
    hit = 0
    if pattern == "":
        return hit
    if len(tags_inner) == 0:
        return hit
    p = "(" + pattern + ")(.*)"
    fit_lists = []
    red_lists = []
    blue_lists = []
    for tag_inner in tags_inner:
        predict_content = tag_inner.get_text()
        match_list = re.findall(p, predict_content)
                
        if len(match_list) > 0:
            hit += 1
            if split:
               [red_str,blue_str] = match_list[0][1].split(split)
               red_list = re.findall(r"\d\d", red_str)
               if red_list not in red_lists:
                    red_lists.append(red_list)
                    Logger.ok("\t\t" + pattern + "\t\t>>> RED" + str(red_list))
               blue_list = re.findall(r"\d\d", blue_str)
               if blue_list not in blue_lists:
                    blue_lists.append(blue_list)
                    Logger.ok("\t\t" + pattern + "\t\t>>> BLUE" + str(blue_list))
            else:
                fit_list = re.findall(r"\d\d", match_list[0][1])
                if fit_list not in fit_lists:
                    fit_lists.append(fit_list)
                    Logger.ok("\t\t" + pattern + "\t\t>>> " + str(fit_list))
    if hit == 0:
        Logger.warn(auther + " Not match " + pattern)
    return hit