import subprocess

# first lets get file info

# this should error since we are calling ffmpeg 
# without an output file arg

file_info = ''

try:
	subprocess.check_output("ffmpeg -i ./sample.mp4", 
				stderr=subprocess.STDOUT, shell=True)

except subprocess.CalledProcessError as e:
	file_info = e.output

file_info = file_info.decode('utf-8')
file_info = file_info.split('\n')

# we want the framerate, which is on line 19
# hope that ffmpeg's output is standard..
# otherwise you'll have to search for the line that starts with
#	"Stream #0:0(und): Video:"

video_info = file_info[18]
fps = video_info.split(',')[4][1:-4] # may have to inspect video_info to get 'fps' lol
# or do some, reverse of the split strings and find whichever starts with spf 
# and then re-reverse


# now to extract
import os
if not os.path.exists('./extracted'): os.mkdir('./extracted')

extract_command = "ffmpeg -i ./sample.mp4 -r {} ./extracted/out-%d.png".format(fps)
subprocess.call(extract_command, shell=True)
