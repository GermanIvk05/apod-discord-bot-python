# APOD-Discord-Bot-Deprecated

Discord bot of the SpaceStop's projects to provide great viewing experience of Astronomy Picture Of the Day and other
NASA resources. The primary goal of the project is to be educational by applying knowledge and skills to build something
great!

#### This project is in early stage of development and any help is appreciated!

We recognise the use of the copyrighted media, thus the project is for non-commercial, personal use, and educational
purposes only. We are currently working on acquiring the permission to use the copyright protected media.

## Installation
Although the Virtual Environment installation is provided below, we are highly suggesting using **Docker** instead for
simplicity of use and the consistency of performance across all systems. The bot is hosted on AWS and **Docker**
provides ease of deployment to cloud.

#### The project uses discord bot token and NASA API key that can be obtained using the links below:
* [Discord Developer Portal (Docs)](https://discord.com/developers/docs/intro)
* [NASA API website](https://api.nasa.gov/)

In the project folder you will find file named `.env.sample` which will contain the sample keys:
```text
DISCORD_TOKEN=".."
NASA_APIKEY=".."
```
1. Create a copy of the file
2. Rename it to `.env`
3. Paste your bot token and NASA API token

Profit! Now you can proceed the installation via **Virtual Environment** or **Docker**.

### Virtual Environment
```sh
python3 -m venv venv
venv\Scripts\activate
pip install --upgrade -r requirements.txt
```

### Docker
```sh
docker-compose up --build
```

## Usage
The **Docker** automatically runs the container when you first build it. For the virtual environment refer to the
command below:
```sh
python3 main.py
```
Now you should see your bot online. Of course make sure to add it to your server first! You should be able to access 3
current commands. Keep in mind the commands are not finalized and are subject to change!

1. `/date` - Fetches the APOD astronomy picture of the day for a specified date.
2. `/random` - Returns a random APOD astronomy picture and its backstory.
3. `/today` - Shows today's APOD-selected astronomical image and its explanation.

We are working on adding more commands to expand the functionality to cover other NASA APIs. Additionally, we have
plans of utilizing GPT-4 to enhance the features provided by our bot.

## Licence
```
MIT License

Copyright (c) 2023 GermanIvk05

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would to change. We are
working on setting up a Discord server for bot feedback and support. This server will be used for contributors and
for ease of communication. More details will be available later.
