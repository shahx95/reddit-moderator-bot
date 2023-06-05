# Reddit Moderator Bot

This is the updated version of my Reddit Moderator Bot, developed after PushShitAPI ceased functioning. It is written in Python and uses the PRAW (Python Reddit API Wrapper) library. This bot is designed to be newbie friendly and takes advantage of Replit's services for seamless operation.  The basic bot performs moderation tasks such as controlling brigading, filtering submissions and comments, removing content from suspicious users, etc. The bot functions can be increased by adding custom functions, which can be as complex as required. I'll add more functions to the functions.py file as I convert them from consuming PushShitAPI to PRAW. 

<p align="center">
  <img alt="matrix gif" src="https://thumbs.gfycat.com/FamousAshamedImperialeagle-size_restricted.gif"/>
</p>


## System Overview
![Reddit Moderator Bot system overview](https://github.com/shahx95/reddit-moderator-bot/assets/24467345/2fc2fabb-4203-4c95-9c64-7788dda6c1db)


## Getting Started

### Prerequisites

- Reddit account with all moderator privileges
- Replit account

### Setup

- Login or sign up on [**Replit**](https://replit.com/)
- Click on **Create Repl**
- Click on **Import From Github** and enter the [link of this repo](https://github.com/shahx95/reddit-moderator-bot)
- If prompted for **Configure entry point**, select `main.py`
- Select the **Secrets** option and click **Edit as Json**
- Copy and paste the following Json object with your Reddit details: 
```
{
"client_id": "enter your account's client ID here",
"client_secret": "enter your client secret here",
"password": "enter your account password here",
"user_agent": "enter your account's app user agent here",
"username": "enter your account's username here",
"mod_sub": "enter the subreddit name where the bot should run"
}
```
- Populate the default values in `main.py` with appropriate information
- In `functions.py`, replace the existing dummy values in banned_word_array with the desired banned words.
- Press CTRL + ENTER or click **Run** to start the bot
- To fix the "PRAW not found" error, run pip install praw in the shell and retry.

## Usage
Once the bot is up and running, it will continuously monitor the specified subreddit for new submissions and comments. The bot will only run for 30 minutes if it doesn't have a webserver being pinged.  To have an **Always On** bot you can buy a Replit personal plan or create a webserver that gets pinged very hour (hint: alive() function in `main.py`) 

## Customization
For detailed information on how each feature works, please consult the code comments and function definitions in the respective files. The bot operates in a modular manner, allowing you to create custom utility functions that can be imported and used seamlessly without disrupting the code flow. Advanced users can leverage this application as a boilerplate to integrate their own features.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
