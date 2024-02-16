FROM python:latest

# set the working directory
WORKDIR /bot

# install dependencies
COPY ./requirements.txt /bot
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY . /bot

# start the bot
CMD ["python3", "main.py"]