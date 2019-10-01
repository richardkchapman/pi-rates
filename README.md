# pi-rates
Raspberry Pi image recognition project

To build the model (on a PC/Mac with Docker installed and running):
docker build -t ell ELL

To extract the build artefacts from the docker image:
id=$(docker create ell)
docker cp $id:/home/hpcc-dev/birdwatcher_pi .

(or you can start the docker image and copy directly from there to your Pi)

Copy these artefacts to your Pi, then (instructions from this point TBD)
