from django.shortcuts import render
from django.conf import settings
#from pytube import YouTube
import os,subprocess
from django.http import HttpResponse,FileResponse
#from youtube_transcript_api import YouTubeTranscriptApi
#from youtube_transcript_api.formatters import WebVTTFormatter
#pip install googletrans==4.0.0-rc1
#from googletrans import Translator
import re


def ytdwn(request,link):
    try:        
        #os.system('sudo apt-get install -y ffmpeg') 
        os.system('yt-dlp  -f 18 -o a.mp4 https://www.youtube.com/watch?v={}'.format(link))        
        tmp4=open('a.mp4' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize('a.mp4')
        response['Content-Disposition'] = 'filename=a.mp4'
        os.remove('a.mp4')
        '''
        video = YouTube('https://www.youtube.com/watch?v=%s' % link)
        stream = video.streams.get_highest_resolution()
        file = str(link)
        media_dir=os.path.join(settings.BASE_DIR,'media')
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
        '''
        return response
    except:
        return HttpResponse ('Youtube Url Is Mistake!')
'''
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
'''
def vid(request):
    try:
        link=request.GET['url']
        os.system('yt-dlp  -f 18 -o a.mp4 {}'.format(link))        
        tmp4=open('a.mp4' , 'rb')
        tmp5=tmp4.read()
        tmp4.close()
        response=HttpResponse(tmp5, content_type='video/mp4')
        response['Content-Length'] = os.path.getsize('a.mp4')
        response['Content-Disposition'] = 'filename=a.mp4'
        os.remove('a.mp4')
        return response
    except:
        return HttpResponse ('Youtube Url Is Mistake!!')
'''
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
'''

def helping(request):
    try:
        return HttpResponse ('''
        <p>Use address of youtube after watch like - for download video -  :<br>
        <b> YourSiteName/ytlink?url=<any video site link></b><br>
        or<br>
        link name like - for play in firefox -  : <br>
        <b>YourSiteName/xazlZh1lTpM</b><br>        
        <a href="/static/ersci_viddown2.xpi">video download firefox Addon</a></br>
        </p>
        ''')
    except:
        return HttpResponse ('Youtube Url Is Mistake!!!')
