# flat-alert
### description
Everybody knows that finding a flat in Berlin is absolute hell.
But you can get access to state-subsidized housing by applying for a WBS (housing entitlement certificate) when your income is low enough.
When you got a WBS you can use inberlinwohnen.de to find your new flat. On this website new ads for cheap flats are
published every day. The problem is that there is no waiting list.
You just apply for each flat and be drawn at random for a chance to move in.
Unfortunately the number of people that can apply for one flat is limited to a few hundred.
So if this number is reached the ad will be offline. This often takes just an hour or less.
So to find your dream apartment you would have to visit inberlinwohnen.de every hour day.

So to solve this problem I created this Telegram bot which will send you notifications if new flats get published.
It scans once every minute 24 hours a day.
You also can set filters about size, price, region, public transport connections and more.

### technology
This program is written as a docker container which can run on every device and can easily be installed.
Personally I have it running on my Raspberry Pi 5 as it does not consume much power.
For scraping the website playwright is being used.
The Google Maps API is being used to calculate how good the flat is connected to important transport hubs by public transport.
Telegram is used to communicate with the user.

### requirements
You need:
* account on inberlinwohnen.de
* telegram bot token
* google maps api key
* docker installed

### project state
This projects primary purpose is my own use so currently it could be hard for non-programmers to change filters and customize the bot.
But I will add these features in the future. Also note that this in very early development stage. I am happy for any contributions.

### quickstart
use these commands to run the program on your machine.

1. download
    ```bash
    git clone https://github.com/eisimo/flat-alert.git && cd flat-alert
    ```

2. now you need to create your .env (see .env.example for reference)

3. and run the container
    ```bash
    docker compose up -d
    ```

### additional information
Tired of filling out these repetitive flat application forms?
I am currently working on another project called [flat-apply](https://github.com/EiSiMo/flat-apply).
It integrates seamlessly into this project on telegram and allows you to automatically apply for flats that flat-alert posted.