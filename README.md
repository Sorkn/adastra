# ad_astra_bot
WHAT IS IT:

It is a telegram bot created to help people find out how good is their location for night sky observations. Type your location, month and time in which you are going to watch the sky and get:

- Address of location

- Your timezone

- Average cloudcover

- Average visibility

- Average humidity

- Light pollution in your location and 100 km around it

- SQM and NELM of your location

If your location placed in the midle of nowhere, you will get a random fact about Chuck Norris as a consolation prize.


*****************

HOW TO USE:

1. Make sure you are registred on the Weather Data Services:
   https://www.visualcrossing.com/weather/weather-data-services#/login

2. Then copy your personal API key and paste in the empty file "TOKEN.txt".

3. After that, create new bot in Telegram. Type \start to BotFather and follow the instructions. Copy token of your new bot and paste in the empty file "BOT_TOKEN.txt"

4. Open cmd and type "cd C:\...\per_aspera_ad_astra"

5. Download requirements:
   - requests
   - Pillow
   - os
   - pyTelegramBotAPI

6. Type "python script.py" in cmd and send "start" to your bot.

7. Enjoy!

*****************

REFERENCES:

Weather data: https://www.visualcrossing.com/weather/weather-data-services

Light pollution map: https://djlorenz.github.io/astronomy/lp2016/

Chuck Norris API: https://api.chucknorris.io/

Telebot documentation: https://github.com/eternnoir/pyTelegramBotAPI
