from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
#pip install moviepy
#script to speed up the video demo
speed=3
video=VideoFileClip("demo.mp4").fx(vfx.speedx,speed)
video.write_videofile("fastdemo.mp4")