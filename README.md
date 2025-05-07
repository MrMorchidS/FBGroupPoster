# FBGroupPoster

## Overview

FBGroupPoster is a lightweight automation tool that posts content to Facebook groups using preconfigured credentials and settings. It supports image and text posting, environment setup via script, and clean logging.

## Modules

- **run.sh**: Sets up the environment, installs dependencies, and launches the application.
- **app.py**: Main application logic – loads config, starts session, and posts to groups.
- **config/**: Stores configuration loader and `config.yaml` for settings like cookies and post content.
- **logger/**: Handles logging for application events.
- **poster/**: Contains the posting logic and session handling.
- **log/**: Stores runtime logs.

## Configuration

Update `config/config.yaml` with your own values:

## How to Run

Make the script executable and run it:

```bash
chmod +x run.sh
./run.sh
```

## What It Does

- Loads your Facebook cookie and post settings from a YAML file.
- Starts a Playwright browser session.
- Posts the image and text to the specified Facebook group IDs.

## Created By

**MrMorchid**  
🔗 [MrMorchid](https://github.com/MrMorchidS)
