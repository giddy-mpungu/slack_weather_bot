# Slack Weather Bot

## Overview
The Weather Slack Bot is a Slack integration that allows users to get current weather information for a specified city right within their Slack workspace. Users can simply use a slash command (`/weather [city]`) to request weather details, and the bot responds with the current temperature in the requested city.

## Features
- Fetches real-time weather data from the OpenWeather API.
- Secure handling of API keys and user inputs.
- Supports temperature conversion to Celsius.
- Simple and intuitive interaction through Slack slash commands.

## Prerequisites
Before using the Weather Slack Bot, make sure you have the following:
- A personal Slack account (free)
- An API key from OpenWeather (free plan available)
- Basic programming skills
- Python installed on your machine

## Getting Started
### Installation
1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.

### Configuration
1. Obtain an API key from [OpenWeather](https://openweathermap.org/) by signing up for a free account.
2. Create a new Slack app in your Slack workspace and configure a slash command (e.g., `/weather`) to point to the server endpoint.
3. Replace the placeholder API key in the `config.py` file with your actual OpenWeather API key.

### Running the Bot
1. Start the server by running `python server.py`.
2. The bot is now listening for incoming requests from Slack.

### Usage
1. In your Slack workspace, type `/weather [city]` to request weather information for a specific city.
2. Wait for the bot to respond with the current temperature in the requested city.

## Testing
The Weather Slack Bot can be tested using tools like Postman or by sending requests directly from the Slack interface.

## Contributing
Contributions are welcome! Please fork this repository and submit pull requests to suggest improvements or fix bugs.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
- [OpenWeather](https://openweathermap.org/) for providing weather data through their API.
- [Slack API](https://api.slack.com/) for enabling bot integration with Slack..

