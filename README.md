# MIC-ISI22-features-monitoring-App
=> achievements:\n
-streaming video using OpenCV and streaminghttpresponse  (3 frames)
-streaming parameters extracted from the video streaming (Velocity monitoring vx,vy,v)
-streaming Statistics of Bubble size monitoring from images extracted from a video feed using channels (pip install channels==3.0.4 )
difficulties:
-streaminghttpresponse and channels don't work together unless there is some kind of synchronization .using Redis or something like it may solve the problem or even trying to stream video using channels.
-the synchronization on WebSockets is not working yet, which means that after the page is refreshed the WebSocket still works in the background but the connection is =>  => disconnected : \n
-the images on the Bubble size monitoring page don't update although the images are updated in the static folders when streaming.
-problems concerning the closing of connecting when a user reloads a page or leaves it. also reconnecting after returning to the same page.
-streaminghttpresponse streams a single video at a time, not 3 at the same time which is not what it should be. that's why better using an alternative way to stream the frames with their parameters at a single channel or request.
-being aware of the versions used to avoid incompatible packages 
.
