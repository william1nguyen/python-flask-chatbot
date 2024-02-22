FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate the environment, and make sure it's activated:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

COPY . /app/
CMD ["python", "app.py"]