import os
from time import sleep
import json
from channels.generic.websocket import WebsocketConsumer
from . import video_model as vid_model, image_model as img_model
from django.core.files.storage import default_storage
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer


class FlotationFrothParameters(WebsocketConsumer):

    def connect(self):
        self.accept()
        print("channel connected")

        pathVideo = "static/app_resources/videos/rl4_pb8-7.mp4"
        cam = vid_model.video_feed(pathVideo)

        for speed_list in vid_model.gen_speed(cam):
            self.send(json.dumps(speed_list))
            sleep(1)

    def disconnect(self, code):
        self.close()
        raise StopConsumer()

    def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('close'):
            self.close()


class ImageProccessStreaming(WebsocketConsumer):

    def connect(self):
        self.accept()
        print("channel connected")
        pathVideo = r"static/app_resources/videos/rl4_pb8-7.mp4"
        for pathout in img_model.extractImages(pathIn=pathVideo):
            try:
                if not os.path.exists(pathout):
                    print('image you trying to proccess does not exist ')

                total_number, list_percentages, list_averages = img_model.image_processus(
                    pathout)

                contexe = {
                    "list_averages": list_averages,
                    "list_percentages": list_percentages,
                    "total_number": total_number
                }
                self.send(json.dumps(contexe))
                sleep(2)
                os.remove(path=pathout)
            except Exception as e:
                print(e)
                self.close()
                break

    def disconnect(self, code):
        self.close()
        raise StopConsumer()

    def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('close'):
            self.close()
