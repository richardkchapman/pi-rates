FROM ubuntu:18.04

RUN apt clean
RUN apt autoclean
RUN apt install -f
RUN apt autoremove
RUN apt-get update

RUN apt-get -y install openssh-server

RUN apt-get -y install tzdata && \
  ln -sf /usr/share/zoneinfo/Europe/Dublin /etc/localtime

RUN apt-get update
RUN apt-get install -y gcc-8 g++-8 cmake libedit-dev zlibc zlib1g zlib1g-dev make
RUN apt-get install -y gnupg2

RUN sh -c 'echo deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-8 main >> /etc/apt/sources.list'
RUN sh -c 'echo deb-src http://apt.llvm.org/bionic/ llvm-toolchain-bionic-8 main >> /etc/apt/sources.list'
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-get update
RUN apt-get install llvm-8 -y

RUN apt-get install -y curl
RUN apt-get install -y g++

RUN curl -O --location http://prdownloads.sourceforge.net/swig/swig-4.0.0.tar.gz
RUN tar zxvf swig-4.0.0.tar.gz
RUN cd swig-4.0.0 && ./configure --without-pcre && make && make install

RUN apt-get install -y git
RUN apt-get install -y libopenblas-dev doxygen unzip sudo

RUN useradd -d /home/hpcc-dev -ms /bin/bash -g root -G sudo -p $(perl -e'print crypt("hpcc-dev", "aa")') hpcc-dev
USER hpcc-dev
WORKDIR /home/hpcc-dev

RUN git clone https://github.com/Microsoft/ELL.git

WORKDIR /home/hpcc-dev/ELL

RUN mkdir build
WORKDIR /home/hpcc-dev/ELL/build

USER root
RUN apt-get install -y python3 python3-dev python3-pip python3-opencv python3-numpy
#RUN pip3 install numpy
#RUN pip3 install opencv-contrib-python
RUN pip3 install flake8

USER hpcc-dev
RUN cmake .. 
RUN make

WORKDIR /home/hpcc-dev
RUN mkdir birdwatcher
WORKDIR /home/hpcc-dev/birdwatcher

RUN curl --location -o model.ell.zip https://github.com/Microsoft/ELL-models/raw/master/models/ILSVRC2012/d_I224x224x3CMCMCMCMCMCMC1AS/d_I224x224x3CMCMCMCMCMCMC1AS.ell.zip
RUN unzip model.ell.zip
RUN mv d_I224x224x3CMCMCMCMCMCMC1AS.ell model.ell
RUN curl --location -o categories.txt https://github.com/Microsoft/ELL-models/raw/master/models/ILSVRC2012/categories.txt

RUN python3 ~/ELL/tools/wrap/wrap.py --model_file model.ell --language python --target host

RUN mkdir host/build
WORKDIR /home/hpcc-dev/birdwatcher/host/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release && make
WORKDIR /home/hpcc-dev/birdwatcher
RUN cp ~/ELL/docs/tutorials/shared/tutorial_helpers.py .
COPY call_model.py /home/hpcc-dev/birdwatcher/call_model.py
COPY coffeemug.jpg /home/hpcc-dev/birdwatcher/coffeemug.jpg

WORKDIR /home/hpcc-dev
RUN mkdir birdwatcher_pi
WORKDIR /home/hpcc-dev/birdwatcher_pi
RUN cp ~/birdwatcher/tutorial_helpers.py . && \
    cp ~/birdwatcher/categories.txt . && \
    python3 ~/ELL/tools/wrap/wrap.py --model_file ~/birdwatcher/model.ell --language python --target pi3
COPY tutorial.py /home/hpcc-dev/birdwatcher_pi/tutorial.py
