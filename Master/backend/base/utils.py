import subprocess
from pytube import YouTube
import os
import uuid
from subprocess import Popen, PIPE
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def get_duration(self):
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(self.input_file_path)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    return round(float(output))
path = os.path.join(settings.MEDIA_ROOT, "temp")
class Video:
    def __init__(self, _file):
        try:
            os.makedirs(path, exist_ok = True)
            print("Directory created successfully" )
        except OSError as error:
            print("Directory can not be created")
        self._file = _file['file']
        self.name="_".join(self._file.name.split())
        self.name=os.path.splitext(str(self._file))[0]
        input_file_extension = os.path.splitext(str(self._file))[1]
        self.input_file_name=str(uuid.uuid1())+input_file_extension
        self.input_file = default_storage.save(self.input_file_name, ContentFile(self._file.read()))
        self.input_file_path = default_storage.path(self.input_file)
        print(self.input_file_path)
        self.length = get_duration(self)        
    def video_to_mp3(self,target_file_extension=".mp3"):
        self.rand=str(uuid.uuid1())
        self.name=self.name+target_file_extension
        file_name=self.rand+target_file_extension
        full_filename = os.path.join(settings.MEDIA_ROOT,'temp',file_name)
        print(full_filename)
        cmd='ffmpeg -i '+self.input_file_path+' '+full_filename
        cmd= Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
        out, err = cmd.communicate()
        if cmd.returncode == 0 :
            print ("Job done.")
        else:
            print ("ERROR")
            print (out)
        self.out_file=full_filename
        default_storage.delete(self.input_file)

class Youtube:
    def __init__(self, url):
        try:
            os.makedirs(path, exist_ok = True)
            print("Directory created successfully" )
        except OSError as error:
            print("Directory can not be created")
        self.url = url
        self.youtube_obj=YouTube(url)
        self.audio = YouTube(url).streams.filter(only_audio=True).first()
        print(self.audio)
        self.name = self.audio.default_filename
        self.name= "_".join(self.name.split())
        self.name=os.path.splitext(str(self.name))[0]
        self.length = self.youtube_obj.length
    
    def youtube_to_mp3(self,target_file_extension=".mp3"):
        self.rand=str(uuid.uuid1())
        self.name=self.name+target_file_extension
        file_name=self.rand+target_file_extension
        out_file = self.audio.download(output_path = 'media/temp',filename=file_name)
        base, ext = os.path.splitext(out_file)
        new_file = base + target_file_extension
        os.rename(out_file, new_file)
        self.file_path=new_file