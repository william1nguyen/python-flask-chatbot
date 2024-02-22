FROM continuumio/miniconda:latest

WORKDIR /home/docker_conda_template

COPY environment.yml ./
COPY static/ ./
COPY templates ./
COPY app.py ./
COPY boot.sh ./

RUN chmod +x boot.sh

RUN conda env create -f environment.yml

RUN echo "source activate mechat" &gt; ~/.bashrc
ENV PATH /opt/conda/envs/mechat/bin:$PATH

EXPOSE 5050

ENTRYPOINT ["./boot.sh"]