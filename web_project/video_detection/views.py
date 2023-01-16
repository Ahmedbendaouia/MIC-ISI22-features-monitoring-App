from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Video_feed
# Create your views here.


@login_required(login_url='login')
def Bubble_size_monitoring_page(request):
    return render(request, 'Bubble_size_monitoring.html')


@login_required(login_url='login')
def Flotation_froth_display_page(request):
    return render(request, 'Flotation_froth_display.html')


@login_required(login_url='login')
def video_feed_page(request):
    videos = Video_feed.objects.all()
    if request.method == 'POST':
        file = request.FILES['video']
        description=request.POST['description']
        video = Video_feed.objects.create(description=description,path=file)
        video.save()

    return render(request,
                  'video_feed_controller.html',
                  context={'video_feeds': videos})


@login_required(login_url='login')
def toggle_in_charge(request, pk):
    my_object = Video_feed.objects.get(pk=pk)
    my_object.is_in_charge = not my_object.is_in_charge
    my_object.save()
    return redirect("video_feed_page")


def delete_video_feed(request,pk):
    instance = get_object_or_404(Video_feed, pk=pk)
    instance.path.delete()
    instance.delete()
    return redirect("video_feed_page")