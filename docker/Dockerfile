FROM ubuntu:latest

ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y wget &&\
  apt-get install -y libglib2.0-dev

RUN apt-get update && apt-get install -y \
  wget \
  libglib2.0-0  \
  libgl1-mesa-glx \
  xcb \
  "^libxcb.*" \
  libx11-xcb-dev \
  libglu1-mesa-dev \
  libxrender-dev \
  libxi6 \
  libdbus-1-3 \
  libfontconfig1 \
  xvfb \
  && rm -rf /var/lib/apt/lists/*

RUN cd root && mkdir temp && cd temp &&\ 
  wget http://coppeliarobotics.com/files/V-REP_PRO_EDU_V3_5_0_Linux.tar.gz &&\
  tar -xvzf V-REP_PRO_EDU_V3_5_0_Linux.tar.gz &&\
  mv V-REP_PRO_EDU_V3_5_0_Linux ../V-REP &&\
  rm -rf temp/*

##### VNC + OPENBOX #####
# Install a VNC X-server, Frame buffer, and windows manager
RUN apt-get update && apt-get install -y x11vnc xvfb openbox obconf

# Finally, install wmctrl needed for bootstrap script
RUN apt-get install -y wmctrl 

# Copy scripts
COPY bootstrap.sh / 
##### END : VNC + OPENBOX #####

CMD '/bootstrap.sh'