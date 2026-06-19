# Steam free games checker project

## Introduction
This python project gets new free games from steam daily and sends an email to the user containing the new free games. It doesn't add these games to any steam profile nor does it send non-free games.

## Setup

1. Check if all files are installed
2. Create a virtual environment in the root folder
3. Start up the venv and install all requirements from requirements.txt
4. Change the user email in `config.json` to your own email

### Commands

- Start .venv from root folder
```Bash
.\.venv\Scripts\Activate.ps1
```

- Install packages from requirements.txt 
```Bash
pip install -r .\Sources\requirements.txt
```

## Project requirements

### Key features

- Automatically check Steam store for free games every day.
- Filter results to show only time-limited free games. 
- Send notifications with game title, link, and end date.
- Keep a short log of already-notified games to avoid repeats.

### Must requirements

- Daily automated checks of the Steam store page. 
- Accurate detection of time-limited free games. 
- E-Mails delivered reliably to me.

### Could requirements

- Provide an option to notify only for games above a minimum review score.
- Offer a small web dashboard to view recent finds.

### Should requirements

- Include game metadata (price history, platform tags).
- Allow configurable notification windows and filters.

### Won't have requirements

- No in-depth pricing analysis or purchase automation.
- No account-based actions on Steam (no login required).

## Project plan

[Project plan](https://develop.pqforce.com/cyril)

## UML diagrams

### UML component diagram

![UML component diagram](..\Design\Component_Diagram.png)

### UML activity diagram

![UML activity diagram](.\UML_Project.png)

## Unittests setup

1. Open the unittests tab
2. Press "Configure Python Tests"
3. Select "Unittest"
4. Select the root folder "."
5. Execute the discovered tests
