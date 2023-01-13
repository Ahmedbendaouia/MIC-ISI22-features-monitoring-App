from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from . import video_model as vid_mod
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login')
def Bubble_size_monitoring_page(request):
    return render(request, 'Bubble_size_monitoring.html')


@login_required(login_url='login')
def Flotation_froth_display_page(request):
    return render(request, 'Flotation_froth_display.html')



@gzip.gzip_page
def spare_frame(request):
    try:
        pathVideo = r"static\app_resources\videos\rl4_pb8-7.mp4"
        cam = vid_mod.video_feed(pathVideo)
        print("spare_frame method is working ........")
        return StreamingHttpResponse(
            vid_mod.gen_spare(cam),
            content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(e)
        print("spare frame Streaming not working !")


@gzip.gzip_page
def Otsu_frame(request):
    try:
        pathVideo = r"static\app_resources\videos\rl4_pb8-7.mp4"
        cam = vid_mod.video_feed(pathVideo)

        return StreamingHttpResponse(
            vid_mod.gen_Otsu(cam),
            content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(e)
        print("Otsu frame streaming is not working !")


@gzip.gzip_page
def flotation_froth_frame(request):
    try:
        pathVideo = r"static\app_resources\videos\rl4_pb8-7.mp4"
        cam = vid_mod.video_feed(pathVideo)

        return StreamingHttpResponse(
            vid_mod.gen_frame(cam),
            content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(e)
        print("flotation froth frame streaming is not working !")


#this is method needs to be repaired
#this method works on streaming data (such as string ,Integer ...) using StreamingHttpResponse and catching it with XMLHttpResponse (AJAX)
#still has some problems to fix , that's why we replace it with Django Channels
def speed_stream(request):
    try:
        pathVideo = r"static\app_resources\videos\rl4_pb8-7.mp4"
        cam = vid_mod.video_feed(pathVideo)
        stream = vid_mod.gen_speed(cam)
        print(stream)
        return StreamingHttpResponse(vid_mod.gen_speed(cam),
                                     status=200,
                                     content_type='text/event-stream')
    except Exception as e:
        print(e)
        print("speed method is not working !")
