# Telegram Data Analysis Bot

## Overview

This is a simple Telegram bot that allows users to send requests in JSON format and receive responses related to data analysis. The bot responds to specific commands and accepts JSON messages for processing.

## Features

- **Start Command**: Users can initiate a conversation with the bot by sending the `/start` command. The bot will provide instructions on how to send data analysis requests in JSON format.

- **Data Analysis**: Users can send JSON messages with specific parameters, and the bot will process these requests using the `generate_response` function and provide the results.

## Getting Started

To use this bot, follow these steps:

1. **Clone repo**:
    ```
   https://github.com/CHRNVpy/rtl_bot.git
   ```

2. **Prerequisites**: You will need Python installed on your system along with the required dependencies. You can install dependencies using pip:

   ```bash
   poetry install
   ```

3. **Bot Token**: Create a bot on Telegram and obtain a bot token. Set the token as an environment variable in a `.env` file:

   ```env
   token=YOUR_BOT_TOKEN
   ```

4. **Run the Bot**: Execute the `main` function to start the bot. This will initialize the bot, set up the dispatcher, and start listening for user requests.

   ```bash
   python bot.py
   ```

5. **Interacting with the Bot**: You can interact with the bot by sending messages to it. Start with the `/start` command to receive instructions on how to format data analysis requests in JSON.

## Usage

- Send a `/start` command to get instructions on how to send data analysis requests.

- To send a data analysis request, format it as a JSON message. For example:

  ```json
  {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}
  ```

- The bot will process the request and provide a response.

## Author

[chrnv](https://t.me/chrnv_dev)
