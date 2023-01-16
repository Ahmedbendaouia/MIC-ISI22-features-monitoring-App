import base64, os, asyncio, json
from . import video_model as vid_model, image_model as img_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from .models import Video_feed
from concurrent.futures import ThreadPoolExecutor


class FlotationFrothParameters(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("stream", self.channel_name)
        await self.accept()
        print("channel connected")

        # Use ThreadPoolExecutor to run the get_video_feed method in a separate thread
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            path = await loop.run_in_executor(executor, self.get_video_feed, True)

        pathVideo = "media/" + str(path)
        
        if not os.path.isfile(pathVideo):
            print("File does not exist")
            self.close()

        cam = vid_model.video_feed(pathVideo)

        for speed_list in vid_model.gen_speed(cam):
            await self.send(json.dumps(speed_list))
            await asyncio.sleep(0.1)

    async def disconnect(self, code):
        print("channel disconnect !!")
        await self.channel_layer.group_discard("stream", self.channel_name)
        raise StopConsumer()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('close'):
            self.close()

    #this is a method to get the path of the video feed from tha database
    def get_video_feed(self, in_charge):
        feed = Video_feed.objects.get(is_in_charge=in_charge)
        return feed.path


class ImageProccessStreaming(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("stream", self.channel_name)
        await self.accept()
        print("channel connected")

        # Use ThreadPoolExecutor to run the get_video_feed method in a separate thread
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            path = await loop.run_in_executor(executor, self.get_video_feed, True)

        pathVideo = "media/" + str(path)
        if not os.path.isfile(pathVideo):
            print("File does not exist")
            self.close()

        for pathout in img_model.extractImages(pathIn=pathVideo):
            try:
                if not os.path.exists(pathout):
                    print('image you trying to proccess does not exist ')

                total_number, list_percentages, list_averages = img_model.image_processus(
                    pathout)

                with open(
                        r'static\app_resources\images\output\segmented_froth_img.png',
                        "rb") as image_file:
                    seg_img = base64.b64encode(image_file.read()).decode()
                with open(
                        r'static\app_resources\images\output\Otsu_thresholding_img.png',
                        "rb") as image_file:
                    otsu_img = base64.b64encode(image_file.read()).decode()
                with open(r'static\app_resources\images\output\shadow_img.png',
                          "rb") as image_file:
                    shad_img = base64.b64encode(image_file.read()).decode()

                contexe = {
                    "seg": seg_img,
                    "otsu": otsu_img,
                    "shad": shad_img,
                    "list_averages": list_averages,
                    "list_percentages": list_percentages,
                    "total_number": total_number
                }
                
                await self.send(json.dumps(contexe, default=str))
                await asyncio.sleep(0.5)
                os.remove(path=pathout)

            except Exception as e:
                print(e)
                await self.close()

    async def disconnect(self, code):
        print("channel disconnect !!")
        await self.channel_layer.group_discard("stream", self.channel_name)
        raise StopConsumer()
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('close'):
            await self.close()

    #this is a method to get the path of the video feed from tha database
    def get_video_feed(self, in_charge):
        feed = Video_feed.objects.get(is_in_charge=in_charge)
        return feed.path
