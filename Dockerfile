# start by pulling the python image
FROM python:3.8-alpine
# FROM python:3.9


# switch working directory
WORKDIR /app

# copy the requirements file into the image
COPY ./requirements.txt .

# install the dependencies and packages in the requirements file
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the exposed port
EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# command to execute
CMD ["run.py" ]

# gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
