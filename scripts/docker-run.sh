docker run \
    -it \
    --rm \
    -w /home \
    -v $PWD/practice:/home \
    continuumio/anaconda3 \
    bash