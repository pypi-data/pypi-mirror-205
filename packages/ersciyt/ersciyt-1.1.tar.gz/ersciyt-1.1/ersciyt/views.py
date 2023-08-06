from django.shortcuts import render
from django.conf import settings
from pytube import YouTube
import os,subprocess
from django.http import HttpResponse,FileResponse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
#pip install googletrans==4.0.0-rc1
#from googletrans import Translator
import re


def ytdwn(request,link):
    try:
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.get_highest_resolution()
        file = str(link)
        media_dir=os.path.join(settings.BASE_DIR,'ytdown','media')
        stream.download(output_path=media_dir,filename=file)
        tmp4=open(media_dir + '/' + file , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.default_filename
        fn=re.sub(r"\s+", '_', fn)
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(media_dir + '/' + file)
        response['Content-Disposition'] = 'filename=%s' % fn
        os.remove(media_dir + '/' + file)
        return response
    except:
        return HttpResponse ('Youtube Url Is Mistake!')

def sub(request,lang,link):
    try:
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.get_highest_resolution()
        media_dir=os.path.join(settings.BASE_DIR,'ytdown','media')
        stream.download(output_path=media_dir,filename='a.mp4')

        #srt=YouTubeTranscriptApi.get_transcript(link)
        transcripts = YouTubeTranscriptApi.list_transcripts(link)
        #if not transcripts :
        #    return HttpResponse('This Video dont have subtitle!')
        transcript = transcripts.find_transcript(['en'])
        if transcript.is_translatable :
            pars = transcript.translate(lang).fetch()
        #else :
        #    return HttpResponse('This Video is not translatable')
        fmt=WebVTTFormatter()
        vtt=fmt.format_transcript(pars)

        f=open(media_dir + '/sub.vtt', 'w', encoding='utf-8')
        f.write(vtt)
        f.close()

        subtitle='subtitles=%s/sub.vtt' % media_dir
        subprocess.run(['ffmpeg','-i', os.path.join(media_dir , 'a.mp4' ),'-vf',subtitle,os.path.join(media_dir,'out.mp4')])

        tmp4=open(media_dir + '/out.mp4' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.default_filename
        fn=re.sub(r"\s+", '_', fn)
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(media_dir + '/out.mp4')
        response['Content-Disposition'] = 'filename=%s' % fn
        os.remove(media_dir + '/a.mp4')
        os.remove(media_dir + '/sub.vtt')
        os.remove(media_dir + '/out.mp4')
        return response
    except:
        return HttpResponse ('This video dont have subtitle !')

def abcut(request,time,link):
    try:
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.get_highest_resolution()
        media_dir=os.path.join(settings.BASE_DIR,'ytdown','media')
        stream.download(output_path=media_dir,filename='a.mp4')

        start_time=time[0:2] + ':' + time[2:4]
        end_time=time[4:6] + ':' + time[6:8]
        subprocess.run(['ffmpeg','-i', os.path.join(media_dir,'a.mp4' ),'-ss',start_time,'-to',end_time,os.path.join(media_dir , 'out.mp4')])

        tmp4=open(media_dir + '/out.mp4' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.default_filename
        fn=re.sub(r"\s+", '_', fn)
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(media_dir + '/out.mp4')
        response['Content-Disposition'] = 'attachment; filename=%s' % fn
        os.remove(media_dir + '/a.mp4')
        os.remove(media_dir + '/out.mp4')
        return response
    except:
        return HttpResponse ('Youtube Url Is Mistake!')

def ytlink(request):
    try:
        link=''
        if request.method == 'GET' and 'url' in request.GET:
            txt = request.GET['url']
            arr = txt.split("watch%3Fv%3D");
            arr1 = arr[-1].split("watch?v=");
            arr2 = arr1[-1].split("&");
            link = arr2[0];

        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.get_highest_resolution()
        media_dir=os.path.join(settings.BASE_DIR,'ytdown','media')
        file = str(link)
        stream.download(output_path=media_dir,filename=file)
        tmp4=open(media_dir + '/' + file , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.default_filename
        fn=re.sub(r"\s+", '_', fn)
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(media_dir + '/' + file)
        response['Content-Disposition'] = 'attachment; filename=%s' % fn
        os.remove(media_dir + '/' + file)
        return response
    except:
        return HttpResponse ('Youtube Url Is Mistake!!')

def ytmp3(request,link):
    try:
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.filter(only_audio=True).first()
        media_dir=os.path.join(settings.BASE_DIR,'ytdown','media')
        file = str(link)
        stream.download(output_path=media_dir,filename=file)
        subprocess.run(['ffmpeg','-i', os.path.join(media_dir, file),os.path.join(media_dir , 'm1.mp3' )])
        tmp4=open(media_dir + '/m1.mp3' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        fn=stream.title + '.mp3'
        fn=re.sub(r"\s+", '_', fn)
        response = HttpResponse(tmp5 , content_type='audio/mp3' )
        response['Content-Length'] = os.path.getsize(media_dir + '/m1.mp3')
        response['Content-Disposition'] = 'attachment; filename=%s' % fn
        os.remove(media_dir + '/' + file)
        os.remove(media_dir + '/m1.mp3')
        return response
    except:
        return HttpResponse (video.description)


def helping(request):
    try:
        return HttpResponse ('''
        <p>Use address of youtube after watch like - for download video -  :<br>
        <b> YourSiteName/ytlink?url=https://www.youtube.com/watch?v=xazlZh1lTpM</b><br>
        or<br>
        link name like - for play in firefox -  : <br>
        <b>YourSiteName/xazlZh1lTpM</b><br>
        and<br>
        for download Mp3 Audio : <br>
        <b>YourSiteName/mp3/xazlZh1lTpM</b><br>
        for download A-B Cutting Video (from 00:30 to 00:70) : <br>
        <b>YourSiteName/ab/00300070/xazlZh1lTpM</b><br>
        for Subtitle the video (for any language enter language code like en,fa,it ) : <br>
        <b>YourSiteName/en/xazlZh1lTpM</b><br>
        <br>
        <a href="/static/epg_youtube4.xpi">YouTube Firefox Addon</a></br>
        </p>
        ''')
    except:
        return HttpResponse ('Youtube Url Is Mistake!!!')
