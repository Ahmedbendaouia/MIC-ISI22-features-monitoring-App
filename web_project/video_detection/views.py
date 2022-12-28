
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import cv2
from . import video_model as model ,image_model as img_mod
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
    

#this is part is under testing

def image_test(request):
    
    total_number, list_percentages, list_averages=img_mod.image_processus()
    
    contexe={"list_averages":list_averages,"list_percentages":list_percentages,"total_number":total_number}
    
    return render(request,'video_detection/image_process.html',contexe)



def test(request):    
    return render(request, 'video_detection/test.html')



#----------------------------------------------------------------------------------------------------------


#home page
@login_required(login_url='login')
def home(request):
    return render(request, 'video_detection/app.html')

        
        
@gzip.gzip_page
def spare_frame(request):
    try:
        pathVideo = "video_detection/statics/videos/rl4_pb8-7.mp4"
        cam = model.video_feed(pathVideo)
        print("spare_frame method is working ........")
        return StreamingHttpResponse(
            model.gen_spare(cam),
            content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("frame  Streaming not  working !!!!!!!!!!!!!!!!!!!!!!!!")


@gzip.gzip_page
def Otsu_frame(request):
    try:
        pathVideo = "video_detection/statics/videos/rl4_pb8-7.mp4"
        cam = model.video_feed(pathVideo)
        print("Otsu_frame method is working ...")
        return StreamingHttpResponse(
            model.gen_Otsu(cam),
            content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("Otsu_frame methode is not working !!!!!!!")


@gzip.gzip_page
def flotation_froth_frame(request):
    try:
        pathVideo = "video_detection/statics/videos/rl4_pb8-7.mp4"
        cam = model.video_feed(pathVideo)
        print("origenal_frame method is working ...")
        return StreamingHttpResponse(model.gen_frame(cam),
            content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("origenal_frame is not working !!!!")


def speed_stream(request):
    try:
        pathVideo = "video_detection/statics/videos/rl4_pb8-7.mp4"
        cam = model.video_feed(pathVideo)    
        stream = model.gen_speed(cam)    
        response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response
    except:        
        print("speed method is not working !!!!!!!!!!!!!!!!!!!!!!!!")