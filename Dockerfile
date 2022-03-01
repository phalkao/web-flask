# start by pulling the python image
FROM python:3.8-alpine

# switch working directory
WORKDIR /app

# copy the requirements file into the image
COPY ./requirements.txt .

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the exposed port
EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# command to execute
CMD ["app.py" ]

# CMD ["gunicorn", "--workers=3". "--bind", "0.0.0.0:5000", "app:app"]
