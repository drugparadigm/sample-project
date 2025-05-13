FROM continuumio/miniconda3

WORKDIR /usr/src/app

COPY . .

# The conda environment should be from the dgx (!!NOT from your PC)

RUN conda env create -f environment.yaml

SHELL ["/bin/bash", "-c"]

RUN conda init bash

RUN chmod +x additional-softwares.sh

# Replace <env-name> with the name of your conda environment
RUN /bin/bash -c "source activate <env-name> && ./additional-softwares.sh"

ENV FLASK_APP=api.py

ENV FLASK_ENV=production

EXPOSE 5000

# Replace <env-name> with the name of your conda environment
CMD [ "bash", "-lc", "source activate <env-name> &&  flask run --host=0.0.0.0 --port=5000" ]