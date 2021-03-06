# chemobot_tools

This is a collection of tools for chemorobotic platform used in the Cronin Group.

Each functionality comes with an example files in the examples folder. To test the examples, first download and install the library: ```python setup.py install``` with appropriate rights. The go to the examples directory and follow the examples.

## video_recorder

video_recorder allows to record a video from a webcam into a file asynchronously. This mean you can keep doing things while the video is recorded.

[[Example and tutorial]](examples/video_recorder/demo.py)


## v4l2

v4l2 is a simple python library to make system call to v4l2-ctl.

v4l2-ctl is tool to read and set parameters of video device, such as focus for webcam, see website: https://www.mankier.com/1/v4l2-ctl
>> The v4l2-ctl tool is used to control video4linux devices, either video, vbi, radio or swradio, both input and output. It is able to control almost any aspect of such devices convering the full V4L2 API.

It is a command line tools for linux. On ubuntu, it can be installed using apt-get: ```sudo apt-get install v4l-utils```

Example commands are:
- list all commands: v4l2-ctl -d 1 -l
- set focus_auto commands: v4l2-ctl -d 1 -c focus_auto=0

This tool allow to start an experiment with always the same webcam config, this is particularly helpful when there is autofocus involved that should be disabled and set manually.

[[Example and tutorial]](examples/v4l2/demo.py)

## droplet_tracking

droplet_tracking is a serie of tool to analyse image and video of droplets

- label_video is a tool to annotate video of droplet. [[Code Example]](examples/droplet_tracking/demo_label_video.py) [[Commands docs](docs/label_video_commands.md)]

## Authors

[Jonathan Grizou](http://www.chem.gla.ac.uk/cronin/members/Jonathan/) while working in the [Cronin Group](http://www.chem.gla.ac.uk/cronin/).

## License

[![GPL V3](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl.html)
