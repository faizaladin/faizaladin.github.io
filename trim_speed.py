import subprocess

# Input and output video files
input_video = "trimmed_flipper.mov"
output_video = "trimmed_flipper_trimmed_spedup.mov"

# Get video height using ffprobe
import json
import shlex
probe_cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=height -of json {shlex.quote(input_video)}"
probe_result = subprocess.run(probe_cmd, shell=True, capture_output=True, text=True)
height = int(json.loads(probe_result.stdout)["streams"][0]["height"])

# Calculate crop values (trim 5% from the top)
trim_percent = 0.1
crop_y = int(height * trim_percent)
crop_h = height - crop_y

# ffmpeg command to crop and speed up video
ffmpeg_cmd = (
	f"ffmpeg -i {shlex.quote(input_video)} "
	f"-filter:v 'crop=in_w:{crop_h}:0:{crop_y},setpts=0.5*PTS' "
	f"-an {shlex.quote(output_video)}"
)

print("Running:", ffmpeg_cmd)
subprocess.run(ffmpeg_cmd, shell=True, check=True)
print(f"Output saved to {output_video}")