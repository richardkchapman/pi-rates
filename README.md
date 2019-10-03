# pi-rates
Raspberry Pi image recognition project

To build the model (on a PC/Mac with Docker installed and running):
docker build -t ell ELL

To extract the build artefacts from the docker image:
id=$(docker create ell)
docker cp $id:/home/hpcc-dev/birdwatcher_pi .

(or you can start the docker image and copy directly from there to your Pi)

For your convenience a precompiled set of these artefacts is checked into this repo.

To set up opencv on the raspberry pi 4, follow the instructions at:

https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/

(the instructions at https://microsoft.github.io/ELL/tutorials/Raspberry-Pi-setup/ seem to not quite work on
 Raspbian Buster, so I would recommend NOT using the conda route suggested there)

Copy the artefacts to your Pi, then follow the instructions from https://microsoft.github.io/ELL/tutorials/Getting-started-with-image-classification-on-the-Raspberry-Pi/ to create the python bindings

At this point if all is well you should be able to run python tutorial.py to classify live video images.



