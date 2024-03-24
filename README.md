# Slack Weather Bot

## Overview
The Weather Slack Bot is a Slack integration that allows users to get current weather information for a specified city right within their Slack workspace. Users can simply use a slash command (`/jumo_weather [city]`) to request weather details, and the bot responds with the current temperature in the requested city.

## Features
- Fetches real-time weather data from the OpenWeather API.
- Secure handling of API keys and user inputs.
- Supports temperature conversion to Celsius.
- Simple and intuitive interaction through Slack slash commands.

## Prerequisites
Before using the Weather Slack Bot, make sure you have the following:
- A personal Slack account (free)
- An API key from OpenWeather (free plan available)
- A ngrok account for tunnelling traffic from the slack API to the local server (free account available)
- Basic programming skills
- Python installed on your machine
- A basic python webserver to host our bot locally.

## Setup

### Slack Integration

1. Create a new Slack app in your Slack workspace.
2. Add a new slash command (e.g., `/jumo_weather`) and configure it to point to the Ngrok URL (will be obtained in the next step) where the bot server is running.
3. Install the Slack app to your workspace.
4. Now you can use the slash command to query weather information from the bot.
![Slack Command Setup](slack_command_setup.png)

### Ngrok Setup

1. Download and install Ngrok from [https://ngrok.com/](https://ngrok.com/).
2. Run Ngrok with the command `ngrok http 8000` (assuming your bot server is running on port 8000).
![Ngrok Setup](ngrok_setup.png)
3. Ngrok will provide you with a public URL that you can use to expose your local server to the internet.
4. Use this Ngrok URL to configure webhook endpoints in your Slack app.
![Ngrok Started](ngrok_started.png)

### OpenWeatherMap API
1. Obtain an API key from [OpenWeather](https://openweathermap.org/) by signing up for a free account.
2. You're sent an email with API key and instruction but you can also find this under "API keys" in your account.
![Open Weather Map Setup](openweathermap_api_setup.png)

## Usage

### Running the Bot
1. Start the server by running `python server.py`.
2. Start ngrok for it to be able to tunnel requests from slack to the local python server.
2. The bot is now listening for incoming requests from Slack.

### UI side
1. In your Slack workspace, type `/jumo_weather [city]` to request weather information for a specific city.
2. Wait for the bot to respond with the current temperature in the requested city.

## Tests

### Understanding APIs

#### OpenWeather API

1. **Exploring OpenWeather API with Postman:**
   - We began by using Postman to directly hit the OpenWeather API and understand the structure of the responses it provides.
   - This helped us determine the necessary parameters and format for making requests to fetch weather data.
![Open Weather Map API Test](test_openweathermap_api.png)

2. **Building the `fetch_weather` Function:**
   - Based on our observations from testing the OpenWeather API, we developed the `fetch_weather` function in `weather.py` to handle requests and parse responses effectively.

#### Slack API

1. **Inspecting Slack API Responses:**
   - To understand how Slack sends requests to our bot, we added print statements in `slack.py` to inspect the raw data received from the Slack API.
   - This allowed us to identify that Slack sends the request data in URL format, which influenced how we processed and formatted the input from the Slack slash command.
![Slack API Test](slack_command_setup.png)


2. **Formatting Slack Slash Command Input:**
   - By analyzing the Slack API responses, we determined the expected format for input parameters, particularly the `text` parameter.
   - We adjusted our code in `slack.py` to extract and format the city parameter correctly before sending it to the OpenWeather API.

3. **Handling Response URLs:**
   - Further examination of the Slack API responses revealed the structure of the `response_url`, indicating where and how to send the weather information back to Slack.
   - This insight guided us in crafting the appropriate response message to be sent back to the user in Slack.

### Conclusion

By thoroughly testing and understanding the behavior of both the OpenWeather and Slack APIs, we were able to develop a Weather Bot that seamlessly integrates with Slack and provides accurate weather information to users.


## Contributing
Contributions are welcome! Please fork this repository and submit pull requests to suggest improvements or fix bugs.

## Acknowledgements
- [OpenWeather](https://openweathermap.org/) for providing weather data through their API.
- [Slack API](https://api.slack.com/) for enabling bot integration with Slack..

