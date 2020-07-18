import os
import re
import librosa
import argparse
import subprocess
from datetime import datetime

subtitles = []
wavs = []
subtitles_file = []
startpoints =[]
finishpoints =[]
filenamecounter = 1
counter = 1
total_number = 0

def getting_sound_and_subtitles(link, directory_audio, directory_subtitles,directory_results):   
    
    global subtitles,wavs,subtitle_file,startpoints,finishpoints,counter

    list_of_videos = "youtube-dl -j --flat-playlist "+link+" | jq -r '.id' | sed 's_^_https://youtu.be/_' >"+directory_results+"videos.txt"
    list_of_videos_str = os.popen(list_of_videos).read()
    with open(directory_results+'videos.txt','r') as videos_in_playlist:
        lots_of_videos_demo = videos_in_playlist.readlines()
    lots_of_videos_demo = list(lots_of_videos_demo)
    for video in lots_of_videos_demo:
        amount_subs = len(os.listdir(directory_subtitles))
        pre_sub = "youtube-dl -i --skip-download --write-sub --sub-lang ru -o '"+directory_subtitles+"%(title)s.%(ext)s'"+" "+video
        sub = os.popen(pre_sub).read()
        new_amount_subs = len(os.listdir(directory_subtitles))
        if amount_subs+1 == new_amount_subs:
            pre_audio = "youtube-dl -i --extract-audio --audio-format wav -o '"+directory_audio+"%(title)s.%(ext)s'"+" "+video
            audio = os.popen(pre_audio).read() 
        else:
            pre_sub = "youtube-dl -i --skip-download --write-auto-sub --sub-lang ru -o '"+directory_subtitles+"%(title)s.%(ext)s'"+" "+video
            sub = os.popen(pre_sub).read()
            another_new_amount_subs = len(os.listdir(directory_subtitles))
            if amount_subs+1 == another_new_amount_subs:
                pre_audio = "youtube-dl -i --extract-audio --audio-format wav -o '"+directory_audio+"%(title)s.%(ext)s'"+" "+video
                audio = os.popen(pre_audio).read()
            else:
                pass  
    
    subtitlesfiles = os.listdir(directory_subtitles)
    for file2 in subtitlesfiles:
        subtitles.append(file2) 
    audiofiles = os.listdir(directory_audio)
    for file1 in audiofiles:
        wavs.append(file1)	
    
    subtitles.sort()
    wavs.sort()
    counter_limit = len(wavs)
    
    for wav in wavs:
        wavdivision(wav,directory_audio,directory_results,directory_subtitles,counter_limit)
        subtitles_file.clear()
        startpoints.clear()
        finishpoints.clear()
    
    print('*preparing next playlist if it exists...')
    wavs.clear()
    subtitles.clear()
    counter_limit=0
    counter=1
    used_wavs = [os.path.join(directory_audio,w) for w in os.listdir(directory_audio)]
    for w in used_wavs:
        os.remove(w) 
    used_subs = [os.path.join(directory_subtitles,s) for s in os.listdir(directory_subtitles)]
    for s in used_subs:
        os.remove(s)
    os.remove(directory_results+'videos.txt')

def subtitlesdivision(file,directory_subtitles):
    
    global subtitles_file,startpoints,finishpoints
    
    with open(directory_subtitles+file, 'r') as subtitles2:
        k = subtitles2.readlines()
    k = list(k) 
    time_moments = []
    for string in k:
        piece_of_time = re.findall('(\d{2}:\d{2}:\d{2}.\d{3}) --> (\d{2}:\d{2}:\d{2}.\d{3})', string) 
        if piece_of_time != []:
            string_index = k.index(string)
            string_index_plus_one = string_index+1
            if k[string_index_plus_one] != []:
                j = k[string_index_plus_one]
                ko = k[string_index_plus_one-1]
                piece_of_time2 = re.findall('(\d{2}:\d{2}:\d{2}.\d{3}) --> (\d{2}:\d{2}:\d{2}.\d{3})', ko)
                j2 = k[string_index_plus_one+1]
                if j2 != []:
                    subtitle = j+j2
                    subtitle = subtitle.lower()
                    subtitle = re.findall(r'([А-я]\w+|[а-я]|[0-9]\d+)', subtitle)
                    subtitle = ' '.join(subtitle)
                    subtitles_file.append(subtitle)
                    time_moments.append(piece_of_time2)
                else:
                    j = j.lower()
                    j = re.findall(r'([А-я]\w+|[а-я]|[0-9]\d+)', j)
                    j = ' '.join(j)
                    subtitles_file.append(j)
                    time_moments.append(piece_of_time2)
                
    for moment in time_moments:
        for time_seconds in moment:
            o1 = re.findall('(\d{2}):(\d{2}):(\d{2}).(\d{3})',time_seconds[0])
            o2 = re.findall('(\d{2}):(\d{2}):(\d{2}).(\d{3})',time_seconds[1])

            for element1 in o1:
                h2 = int(element1[0])
                m2 = int(element1[1])
                s2 = int(element1[2])
                ms2 = (int(element1[3])) * 1000
                g1 = datetime(2019, 5, 6, 0, 0, 0, 0)
                g2 = datetime(2019, 5, 6, h2, m2, s2, ms2)
                g3 = (g2 - g1)
                g51 = g3.total_seconds()
                startpoints.append(g51)

            for element2 in o2:
                g1 = datetime(2019, 5, 6, 0, 0, 0, 0)
                h22 = int(element2[0])
                m22 = int(element2[1])
                s22 = int(element2[2])
                ms22 = (int(element2[3])) * 1000
                g22 = datetime(2019, 5, 6, h22, m22, s22, ms22)
                g32 = (g22 - g1)
                g52 = g32.total_seconds()
                finishpoints.append(g52)

def wavdivision(sound,directory_audio,directory_results,directory_subtitles,counter_limit):
    
    global subtitles,filenamecounter,subtitles_file,startpoints,finishpoints,counter
    
    for textfile in subtitles:
        subtitlesdivision(textfile,directory_subtitles)
        subtitles.remove(textfile)
        break
    y, sr = librosa.load(directory_audio+sound,mono=True)

    def finalmoment(start,finish,filenamecounter):
        j = y[int(start)*sr:int(finish)*sr]                                  
        os.chdir(directory_results+new_folder)
        librosa.output.write_wav(str(filenamecounter)+'.wav', j, sr)
        for subtitletext in subtitles_file:
            new_file_name_for_text = str(filenamecounter)+'.txt'
            with open(new_file_name_for_text, 'w') as gh:
                gh.write(subtitletext)
            subtitles_file.remove(subtitletext)
            break
        
    os.chdir(directory_results)
    new_folder = str(sound)
    os.mkdir(new_folder)
    os.chdir(directory_results+new_folder)

    for moment1,moment2 in zip(startpoints,finishpoints):
        finalmoment(moment1, moment2,filenamecounter)
        filenamecounter += 1
    print ('*',counter,' from ',counter_limit)
    counter+=1



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--playlist_file', dest='URL_list', type=str,
                        help='playlists txt-file path', required=True)
    parser.add_argument('-a', '--audio_path', dest='directory_audio', type=str,
                        help='path to download audiotracks', required=True)
    parser.add_argument('-s','--subs_path', dest='directory_subtitles', type=str,
                        help='path to download subtitles', required=True)
    parser.add_argument('-r', '--results_path', dest='directory_results', type=str,
                        help='path for results', required=True)

    args = parser.parse_args()

    directory_audio = os.path.abspath(args.directory_audio)+'/'
    directory_subtitles = os.path.abspath(args.directory_subtitles)+'/'
    directory_results = os.path.abspath(args.directory_results)+'/'
    URL_list = os.path.abspath(args.URL_list)

    with open(URL_list, 'r') as playlists_links:
        lots_of_videos = playlists_links.readlines()
    lots_of_videos = list(lots_of_videos)
    for i in lots_of_videos:
        i = re.sub("\n", '', i)
        if i=='':
            pass
        else:
            getting_sound_and_subtitles(i,directory_audio, directory_subtitles,directory_results) 
    print('*End. Your files are in '+directory_results+'. If you want to use audiocorpusbuilder again, please, make sure that all of your directories are clear!')  




