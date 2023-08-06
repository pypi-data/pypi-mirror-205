import sys
import os
import time
import requests
import zipfile
import json
from ttauto_crawler import utils
from ttauto_crawler import txt2proj
from template_generator import binary as genertor_binary
import logging
import urllib3
import datetime
import shutil
import subprocess
import random
from urllib.parse import *
from PIL import Image
from fake_useragent import UserAgent
import uuid
import calendar

rootDir = ""
curGroupId = 0
allCount = 0
successCount = 0
maxDownloadCount = 1000
splitZipCount = 200

def clearDir():
    s = os.path.join(rootDir, ".download")
    if os.path.exists(s):
        shutil.rmtree(s)
    s1 = os.path.join(rootDir, ".out")
    if os.path.exists(s1):
        shutil.rmtree(s1)

def curDownloadDir():
    s = os.path.join(rootDir, ".download", str(curGroupId))
    if os.path.exists(s) == False:
        os.makedirs(s)
    return s

def curOutputDir():
    s = os.path.join(rootDir, ".out", str(curGroupId))
    if os.path.exists(s) == False:
        os.makedirs(s)
    return s
    
def notifyMessage(ossurl, count):
    try:
        param = {
            "id": curGroupId,
            "video_path": ossurl,
            "video_num": count
        }
        s = requests.session()
        s.headers.update({'Connection':'close'})
        res = s.post(f"https://beta.2tianxin.com/common/admin/tta/get_set_task_complete", json.dumps(param), verify=False)
        if res.status_code == 200:
            logging.info(f"notifyMessage success")
        else:
            resContext = res.content.decode(encoding="utf8", errors="ignore")
            logging.info(f"notifyMessage fail! code={res.status_code}, context={resContext}")
            print(f"report error!, postdata = {json.dumps(param)}")
        s.close()
    except Exception as e:
        logging.info(f"notifyMessage exception :{e}")

def secondToDuration(d):
    hour = int(d / 3600)
    sec = float(d % 60)
    min = int((d - sec) % 3600 / 60)
    hour_str = str(hour).rjust(2).replace(" ", "0")
    min_str = str(min).rjust(2).replace(" ", "0")
    sec_str = ""
    if sec > 10:
        sec_str = str(sec)
    else:
        sec_str = f"0{str(sec)}"
    return f"{hour_str}:{min_str}:{sec_str}"

def processAllImage(data, addRandomText, img2videoCnt):
    src = curDownloadDir()
    dst = curOutputDir()
    s = []
    for root,dirs,files in os.walk(src):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")].lower()
            ext = file[file.index("."):].lower()
            if ext in [".jpg", ".png", ".jpeg", ".bmp"]:
                s.append(os.path.join(root, file))
        if root != files:
            break
    templates = []
    while len(s) > img2videoCnt:
        s1 = []
        allcnt = len(s)
        for i in range(img2videoCnt):
            rd_idx = random.randint(0, allcnt-1)
            tmp_s = s[rd_idx]
            s.remove(tmp_s)
            allcnt -= 1
            s1.append(tmp_s)
        templates.append(txt2proj.imgsToTemplate(s1, addRandomText))
        
    idx = 0
    for tp in templates:
        data.append({
                "input":[],
                "template": tp,
                "params":{},
                "output": os.path.join(dst, f"img2video_{idx}.mp4")})
        idx+=1

def videoToTemplate(data, tpname, addRandomText, splitDuration):
    src = curDownloadDir()
    dst = curOutputDir()
    templateDir = ""
    if len(tpname) > 0:
        templateDir = os.path.join(genertor_binary.randomEffectPath(""), tpname)
    for root,dirs,files in os.walk(curDownloadDir()):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".mp4":
                w,h,bitrate,fps,video_duration = utils.videoInfo(os.path.join(src, file))
                if w <= 0 or bitrate <= 0:
                    continue
                srcVideo = os.path.join(src, f"{name}{ext}")
                dstVideo = os.path.join(dst, f"{name}_{tpname}{ext}")
                if splitDuration > 0 and video_duration > splitDuration * 1.5:
                    idx = 0
                    while (idx * splitDuration) < video_duration:
                        split_duration = splitDuration
                        if ((idx+1) * splitDuration) > video_duration:
                            split_duration = video_duration - (idx * splitDuration)
                        if split_duration < splitDuration / 2:
                            #ignore too short slice
                            break
                        tmpPath = os.path.join(curDownloadDir(), f"{name}_autoremove_{idx}.mp4")
                        dstVideo = os.path.join(dst, f"{name}_{idx}_{tpname}{ext}")
                        if os.path.exists(tmpPath) == False:
                            cmd = f"-i {srcVideo} -ss {secondToDuration(idx * splitDuration)} -t {secondToDuration(split_duration)} -y {tmpPath}"
                            logging.info(f"=============== ffmpeg {cmd}")
                            utils.ffmpegProcess(cmd)
                        if os.path.exists(tmpPath):
                            realTemplateDir = templateDir
                            if addRandomText and tpname != "template8":
                                if len(templateDir) > 0:
                                    tempDir = txt2proj.newTemplateWithText(templateDir, w, h, split_duration)
                                else:
                                    tempDir = txt2proj.singleVideoToTemplate(tmpPath, True, False, w, h, split_duration)
                                realTemplateDir = tempDir
                            if len(realTemplateDir):
                                data.append({
                                    "input":[tmpPath],
                                    "template": realTemplateDir,
                                    "params":{},
                                    "output": dstVideo})
                            else:
                                shutil.copyfile(tmpPath, dstVideo)
                        idx+=1
                else:
                    realTemplateDir = templateDir
                    if addRandomText:
                        if len(templateDir) > 0:
                            tempDir = txt2proj.newTemplateWithText(templateDir, w, h, video_duration)
                        else:
                            tempDir = txt2proj.singleVideoToTemplate(srcVideo, True, False, w, h, video_duration)
                        realTemplateDir = tempDir
                    if len(realTemplateDir):
                        data.append({
                            "input":[srcVideo],
                            "template": realTemplateDir,
                            "params":{},
                            "output": dstVideo})
                    else:
                        shutil.copyfile(srcVideo, dstVideo)
        if root != files:
            break

def processToVideo(crawler_template_name, addRandomText, splitDuration, img_to_video, video_merge_num, video_merge_second):
    src = curDownloadDir()
    dataFile = os.path.join(src, "params.config")
    data = []
    official_template_list = []
    if len(crawler_template_name) > 0:
        for tpname in crawler_template_name:
            templateDir = os.path.join(genertor_binary.randomEffectPath(""), tpname)
            official_template_list.append(templateDir)
            videoToTemplate(data, tpname, addRandomText, splitDuration)
    else:
        videoToTemplate(data, "", addRandomText, splitDuration)
    
    if img_to_video > 0:
        processAllImage(data, addRandomText, img_to_video)
    if len(data) > 0:
        with open(dataFile, 'w') as f:
            json.dump(data, f)
        try:
            print(f"template --input {dataFile} --adaptiveSize")
            result = subprocess.run(f"template --input {dataFile} --adaptiveSize", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if result.returncode == 0:
                print("=== process success")
                for it in data:
                    if it["template"] not in official_template_list:
                        shutil.rmtree(it["template"])
                os.remove(dataFile)
            else:
                print("====================== script error ======================")
                print(result.stderr.decode(encoding="utf8", errors="ignore"))
                print("======================     end      ======================")
        except subprocess.CalledProcessError as e:
            print("====================== process error ======================")
            print(e)
            print("======================      end      ======================")
    
def download(name, media_type, post_text, media_resource_url, audio_resource_url):
    ext = ".mp4"
    if media_type == "image":
        ext = ".jpg"
    elif media_type == "audio":
        ext = ".mp3"
    savePath = os.path.join(curDownloadDir(), f"{name}{ext}")
    if os.path.exists(savePath):
        os.remove(savePath)
    #download
    logging.info(f"download: {media_resource_url}, {audio_resource_url}")
    s = requests.session()
    s.headers.update({'Connection':'close'})
    ua = UserAgent()
    download_start_pts = calendar.timegm(time.gmtime())
    file = s.get(media_resource_url, verify=False, headers={'User-Agent': ua.random})
    with open(savePath, "wb") as c:
        c.write(file.content)
    download_end_pts = calendar.timegm(time.gmtime())
    logging.info(f"download duration={(download_end_pts - download_start_pts)}")
    #merge audio & video
    if len(audio_resource_url) > 0:
        audioPath = os.path.join(curDownloadDir(), f"{name}.mp3")
        file1 = s.get(audio_resource_url)
        with open(audioPath, "wb") as c:
            c.write(file1.content)
        tmpPath = os.path.join(curDownloadDir(), f"{name}.mp4.mp4")
        utils.ffmpegProcess(f"-i {savePath} -i {audioPath} -vcodec copy -acodec copy -y {tmpPath}")
        if os.path.exists(tmpPath):
            os.remove(savePath)
            os.rename(tmpPath, savePath)
            os.remove(audioPath)
        logging.info(f"merge => {file}, {file1}")
    s.close()
    
def processPosts(uuid, data):
    global allCount

    post_text = data["text"]
    medias = data["medias"]
    idx = 0
    for it in medias:
        media_type = it["media_type"]
        media_resource_url = it["resource_url"]
        audio_resource_url = ""
        if "formats" in it:
            formats = it["formats"]
            quelity = 0
            for format in formats:
                if format["quality"] > quelity and format["quality"] <= 1080:
                    quelity = format["quality"]
                    media_resource_url = format["video_url"]
                    audio_resource_url = format["audio_url"]
        try:
            allCount += 1
            download(f"{uuid}_{idx}", media_type, post_text, media_resource_url, audio_resource_url)
            time.sleep(1)
        except Exception as e:
            print("====================== download+process+upload error! ======================")
            print(e)
            print("======================                                ======================")
            time.sleep(10) #maybe Max retries
        idx += 1

def aaaapp(multiMedia, url,  cursor, page):
    if len(url) <= 0:
        return
    
    param = {
        "userId": "D042DA67F104FCB9D61B23DD14B27410",
        "secretKey": "b6c8524557c67f47b5982304d4e0bb85",
        "url": url,
        "cursor": cursor,
    }
    requestUrl = "https://h.aaaapp.cn/posts"
    if multiMedia == False:
        requestUrl = "https://h.aaaapp.cn/single_post"
    logging.info(f"=== request: {requestUrl} cursor={cursor}")
    s = requests.session()
    s.headers.update({'Connection':'close'})
    res = s.post(requestUrl, params=param, verify=False)
    with open(os.path.join(curDownloadDir(), "config.txt"), mode='a') as configFile:
        configFile.write(f'\n {res.content} \n')
    if len(res.content) > 0:
        data = json.loads(res.content)
        if data["code"] == 200:
            idx = 0
            if multiMedia == False:
                processPosts(f"{curGroupId}_{page}_{idx}", data["data"])
                if allCount > maxDownloadCount:
                    print(f"stop mission with out of cnt={maxDownloadCount}")
                    return
            else:
                posts = data["data"]["posts"]
                for it in posts:
                    processPosts(f"{curGroupId}_{page}_{idx}", it)
                    if allCount > maxDownloadCount:
                        print(f"stop mission with out of cnt={maxDownloadCount}")
                        return
                    idx+=1
            if "has_more" in data["data"] and data["data"]["has_more"] == True:
                next_cursor = ""
                if "next_cursor" in data["data"] and len(str(data["data"]["next_cursor"])) > 0:
                    if "no" not in str(data["data"]["next_cursor"]):
                        next_cursor = str(data["data"]["next_cursor"])
                if len(next_cursor) > 0:
                    aaaapp(multiMedia, url, next_cursor, page+1)
        else:
            print(f"=== error aaaapp, context = {res.content}")
            logging.info(f"=== error aaaapp, context = {res.content}")
            if data["code"] == 300:
                print("=== no money, exit now!")
                logging.info("=== no money, exit now!")
                exit(-1)
    else:
        print("=== error aaaapp, context = {res.content}, eixt now!")
        logging.info("=== error aaaapp, context = {res.content}, eixt now!")
        exit(-1)
    s.close()

def ftpdownload(url):
    return ""

def cacheDir():
    src = curDownloadDir()
    dist = os.path.join(os.path.dirname(src), f"{curGroupId}.zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 
    for rt,dirs,files in os.walk(src):
        for file in files:
            if str(file).startswith("~$"):
                continue
            if "autoremove" in file:
                continue
            filepath = os.path.join(rt, file)
            writepath = os.path.relpath(filepath, src)
            zip.write(filepath, writepath)
    zip.close()
    shutil.copyfile(dist, f"d://{curGroupId}.zip")
    os.remove(dist)

    dst = curOutputDir()
    dist1 = os.path.join(os.path.dirname(dst), f"{curGroupId}_out.zip")
    zip1 = zipfile.ZipFile(dist1, "w", zipfile.ZIP_DEFLATED) 
    for rt,dirs,files in os.walk(dst):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(rt, file)
            writepath = os.path.relpath(filepath, dst)
            zip1.write(filepath, writepath)
    zip1.close()
    shutil.copyfile(dist1, f"d://{curGroupId}_out.zip")
    os.remove(dist1)

def process(url, crawler_template_name, addRandomText, splitDuration, img_to_video, video_merge_num, video_merge_second):
    global successCount
    ### downlaod
    print(f"=== downloading ")
    if "http" in url:
        isMulti = True
        realUrl = url
        if "Single" in url:
            realUrl = url.replace("Single", "")
            isMulti = False
        aaaapp(isMulti, realUrl, "", 0)
    else:
        ftpdownload(url)
    print(f"=== processing video")
    processToVideo(crawler_template_name, addRandomText, splitDuration, img_to_video, video_merge_num, video_merge_second)
    cacheDir() #cache file to d://
    ### upload + notify
    print(f"=== uploading + notifying ")
    splitCount = 0
    packageIndex = 0
    dist = os.path.join(os.path.dirname(curOutputDir()), f"{curGroupId}_{packageIndex}.zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 
    for rt,dirs,files in os.walk(curOutputDir()):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(rt, file)
            writepath = os.path.relpath(filepath, curOutputDir())
            zip.write(filepath, writepath)
            splitCount+=1
            successCount+=1
            if splitCount >= splitZipCount and (len(files) - successCount > (splitZipCount / 2)):
                zip.close()
                onePackage_ossurl = utils.ftpUpload(dist)[0]
                print(f"=== sending {packageIndex} package ")
                notifyMessage(onePackage_ossurl, splitCount)
                packageIndex+=1
                splitCount = 0
                dist = os.path.join(os.path.dirname(curOutputDir()), f"{curGroupId}_{packageIndex}.zip")
                zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED)
        if rt != files:
            break

    if splitCount > 0:
        zip.close()
        lastPackage_ossurl = utils.ftpUpload(dist)[0]
        print(f"=== sending {packageIndex} package ")
        notifyMessage(lastPackage_ossurl, splitCount)

def lastTaskFile():
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(thisFileDir, "last_task.txt")

def removeLastTask():
    file = lastTaskFile()
    if os.path.exists(file):
        os.remove(file)

def getLocalTask():
    file = lastTaskFile()
    data = {}
    if os.path.exists(file):
        with open(file, 'r', encoding='UTF-8') as f:
            data = json.load(f)
    return data

def saveLastTask(data):
    file = lastTaskFile()
    with open(file, 'w') as f:
        json.dump(data, f)

def getTask():
    data = getLocalTask()
    if len(data) == 0:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        res = s.get(f"https://beta.2tianxin.com/common/admin/tta/get_task?t={random.randint(100,99999999)}", verify=False)
        s.close()
        if len(res.content) > 0:
            data = json.loads(res.content)
            saveLastTask(data)
    return data

def autoCrawler():
    global rootDir
    global curGroupId
    global allCount
    global successCount
    
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    rootDir = thisFileDir
    while(os.path.exists(os.path.join(thisFileDir, "stop.now")) == False):
        try:
            data = getTask()
            if len(data) > 0 and "id" in data:
                curGroupId = data["id"]
                allCount = 0
                successCount = 0
                start_pts = calendar.timegm(time.gmtime())
                logging.info(f"================ begin {curGroupId} ===================")
                logging.info(f"========== GetTask: {data}")
                print(f"=== begin {curGroupId}")
                url = data["url"].replace("\n", "").replace(";", "").replace(",", "").strip()
                template_name_list = data["template_name_list"]
                if template_name_list == None:
                    template_name_list = []
                video_merge_num = int(data["video_merge_num"])
                video_merge_second = int(data["video_merge_second"])
                img_to_video = int(data["img_to_video"])
                split_video = int(data["split_video"])
                add_text = int(data["add_text"])

                clearDir()
                process(url, template_name_list, add_text, split_video, img_to_video, video_merge_num, video_merge_second)

                current_pts = calendar.timegm(time.gmtime())
                print(f"complate => {curGroupId} rst={successCount}/{allCount} duration={(current_pts - start_pts)}")
                logging.info(f"================ end {curGroupId} rst={successCount}/{allCount} duration={(current_pts - start_pts)}===================")
            removeLastTask()
        except Exception as e:
            logging.error("====================== uncatch Exception ======================")
            notifyMessage("", 0)
            logging.error(e)
            logging.error("======================      end      ======================")
        time.sleep(10)
    os.remove(os.path.join(thisFileDir, "stop.now"))
    print(f"stoped !")

# urllib3.disable_warnings()
# d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
# thisFileDir = os.path.dirname(os.path.abspath(__file__))
# logging.basicConfig(filename=f"{thisFileDir}/ttauto_crawler_{d}.log", 
#                     format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     encoding="utf-8",
#                     level=logging.DEBUG)
# rootDir = thisFileDir

# data = {
#     "0": "https://www.douyin.com/user/MS4wLjABAAAAVUVt5ZSw6StLpRpUJPBpL1CGkkjfYF4wKb1MMwXKPS2ys_fr4vCfp3UmmULOVtTy",
# }
# # maxDownloadCount = 2
# splitZipCount = 10
# for k in data:
#     curGroupId = int(k)
#     allCount = 0
#     successCount = 0
#     start_pts = calendar.timegm(time.gmtime())
#     logging.info(f"================ begin {curGroupId} ===================")
#     print(f"=== begin {curGroupId}")
#     url = data[k]
#     crawler_template_name = []
#     process(url, crawler_template_name, False, 15, 0, 0, 0)
#     current_pts = calendar.timegm(time.gmtime())
#     print(f"complate => {curGroupId} rst={successCount}/{allCount} duration={(current_pts - start_pts)}")
#     logging.info(f"================ end {curGroupId} ===================")

