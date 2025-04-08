# Google Sheets AI Bot

A Telegram bot that connects to Google Sheets and uses AI to interact with and manage your spreadsheets through natural language commands.

## Overview

Google Sheets AI Bot allows you to manage any Google Sheet through a Telegram interface powered by OpenAI's GPT models. Originally designed for tracking gym progress, this bot has evolved to work with any spreadsheet, making it a versatile tool for various tracking needs including fitness, finances, projects, and more.

## Features

- 🤖 **AI-Powered Interaction**: Use natural language to read, update, and manage your Google Sheets
- 📱 **Telegram Interface**: Access and modify your sheets from anywhere using Telegram
- 📊 **Multi-Sheet Support**: Work with multiple sheets/tabs within a single Google Spreadsheet
- 🔄 **Customizable AI Behavior**: Set custom system prompts to tailor the AI assistant for your specific use case
- 🔒 **Private Access**: Bot is configured to only allow authorized users

## Google Sheets Integration

The bot leverages Google Sheets API for powerful spreadsheet management:

- **Read Sheet Data**: Access and view data from any tab in your Google Sheet
- **Write to Cells**: Update individual cell values with new data
- **Batch Updates**: Modify multiple cells in a single operation for efficiency
- **Sheet Discovery**: List all available tabs in your spreadsheet
- **Cell Search**: Find specific content within your sheets
- **Formatted Output**: Receive structured, easy-to-read responses about your sheet data

All operations are performed securely using OAuth2 authentication with the Google Sheets API.

## How It Works

1. The bot connects to your Google Sheet using the Google Sheets API
2. You interact with the bot through Telegram, sending natural language requests
3. The bot uses OpenAI's GPT model to interpret your requests and determine the necessary actions
4. It then performs the requested operations on your Google Sheet and responds with the results

## Use Cases

- **Fitness Tracking**: Update workout progress, log weights and reps, track personal records
- **Financial Management**: Track expenses, income, budgets, and financial goals
- **Project Management**: Update task statuses, deadlines, and notes
- **Habit Tracking**: Log daily habits, streaks, and progress towards goals
- **Any spreadsheet-based tracking**: The bot is flexible and can be adapted to most tracking needs

## Quick Setup

### Prerequisites
- Python 3.7+
- Google account with Google Sheets API enabled
- OpenAI API key
- Telegram account

### Configuration
1. Clone this repository
2. Create a `secrets.py` file with your API keys:
   ```python
   open_ai_key = "your-openai-api-key"
   token = "your-telegram-bot-token"
   authorized_user_id = "your_telegram_user_id"
   ```
3. Download your Google API credentials to `credentials.json`
4. Run `python bot.py` to start the bot

## Usage

Start the bot on Telegram with `/start`, enter your Google Sheet ID, set a system prompt, and begin interacting with your spreadsheet using natural language!

### Example Commands

- "Show me my workout plan for this week"
- "Update my bench press weight to 185 lbs for today"
- "List all the tabs in my spreadsheet"
- "Show me the contents of the 'Budget' tab"
- "Update cell B5 to 'Completed'"

### Bot Commands

- `/start` - Initialize the bot and set up your Google Sheet
- `/sheet` - Change the Google Sheet ID
- `/prompt` - Update the system prompt for the AI

## Project Structure

- `main.py` - Main entry point for the Telegram bot
- `ai_control/` - Handles interactions with OpenAI API
- `commands/` - Bot command handlers
- `sheets/` - Google Sheets API interaction functions
- `state.py` - Global state management
