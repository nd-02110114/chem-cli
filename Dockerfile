From continuumio/anaconda3

RUN /opt/conda/bin/conda install jupyter -y --quiet &&  mkdir /opt/notebooks

# 必要なライブラリのImport
RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx