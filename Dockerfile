FROM continuumio/miniconda3

WORKDIR /usr/src/app

COPY . .

RUN apt-get update &&\
        apt-get install -y tzdata && \
        ln -snf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime &&  \
        echo "Asia/Kolkata" > /etc/timezone && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*
 
ENV TZ=Asia/Kolkata

# The conda environment should be from the dgx (!!NOT from your PC)

RUN conda env create -f environment.yaml && conda clean -afy && rm -rf ~/.cache

SHELL ["/bin/bash", "-c"]

RUN conda init bash

RUN chmod +x additional-softwares.sh

# Replace <env-name> with the name of your conda environment
RUN /bin/bash -c "source activate <env-name> && ./additional-softwares.sh && conda clean -afy && rm -rf ~/.cache"


EXPOSE 5000

# Replace <env-name> with the name of your conda environment
CMD [ "bash", "-lc", "source activate <env-name> && exec gunicorn api:app -b 0.0.0.0:5000 --workers=1 --threads=5  --access-logfile -" ]