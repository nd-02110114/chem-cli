docker run \
    -i -t \
    -p 8888:8888 \
    --name jupyter-notebook \
    -v $PWD/practice:/opt/notebooks \
    continuumio/anaconda3 \
    /bin/bash -c "/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --no-browser --allow-root"