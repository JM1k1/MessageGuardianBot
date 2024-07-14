<h1 align='center'>
  <br>
  <img src='https://imgur.com/0jRy6PI.png' width=500 weigth=500 alt='QRKot'>
</h1>
<h1 align='center'>Message Guardan</h4>
<p align='center'>
  <img src="https://img.shields.io/badge/Python-0A0A0A?style=for-the-badge&logo=Python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-0A0A0A?style=for-the-badge&logo=SQLAlchemy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Telethon-0A0A0A?style=for-the-badge&logo=telegram&logoColor=white"/>
</p>

---

Message Guardian Bot is a Telegram bot designed to manage messages in groups, including saving messages, tracking changes, and restoring deleted messages.
The bot is built using the Telethon framework for handling Telegram updates and SQLAlchemy for database interactions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)
- [Contributors](#contributors)

## Installation

1. Clone this repository:

```
git clone git@github.com/JM1k1/MessageGuardianBot.git
```

2. Cd into MessageGuardianBot:

```
cd MessageGuardianBot
```

3. Install [Python 3.11+](https://www.python.org/downloads//)

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3 -y
sudo apt install python3-pip -y
```

4. Install [Poetry](https://python-poetry.org/docs/):

```
curl -sSL https://install.python-poetry.org | python3 -
```

7. Install all dependencies:

```
poetry install
```

## Usage

1. Configure your environment variables. Create a .env file in the root directory of the project and add the following:

```
TELEGRAM_TOKEN=YOUR_TOKEN
FORWARD_CHAT_ID=YOUR_FORWARD_CHAT_ID
DATABASE_ENGINE=sqlite+aiosqlite:///database.db
```

2. Initialize the database:

```
poetry run alembic upgrade head
```

3. Run the bot:

```
poetry run python /src/application.py
```

## Project Structure

### [src](src)

- [application.py](src/application.py): Main entry point for running the bot.
- [client.py](src/dispatcher.py): Configures and starts the Telethon client.

### [src/bot](src/bot)

- [handlers.py](src/bot/handlers.py): Handlers for processing different types of messages.
- [logs/](src/bot/logs): Directory containing logs.

### [src/bot/core](src/bot/core)

- [logger.py](src/bot/core/logger.py): Configures logging for the application.
- [settings.py](src/bot/core/settings.py): Contains configuration settings, including the bot token.

### [src/bot/database](src/bot/database)

- [crud.py](src/bot/database/crud.py): Contains CRUD operations for interacting with the database.
- [database.py](src/bot/database/database.py): Database setup and session management.
- [models.py](src/bot/database/models.py): SQLAlchemy models for the database schema.

### [src/bot/database/migrations](src/bot/database/migrations)

- [env.py](src/bot/database/migrations/env.py): Alembic environment configuration file.
- [script.py.mako](src/bot/database/migrations/script.py.mako): Template for new migration scripts.
- [versions/](src/bot/database/migrations/versions): Directory containing migration scripts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributors

For anyone who is interested in contributing to MessageGuardianBot, please make sure you fork the project and make a pull request.
