# schwab-py-webframework-reference-design
Intended reference design for a practical example of using [schwab-py](https://github.com/alexgolec/schwab-py/tree/main) in a working web application (web framework).  

***As a note:*** This codebase not officially associated with 'schwab-py'.  

***Disclaimer:*** We claim no responsibility for keeping up-to-date with changes in 'schwab-py' in this reference design.  However, the intent is to demonstrate in simple terms how to "create a working web application" using the 'schwab-py' API abstraction library which is built in Python.

## Requirements

- Python3
- [schwab-py](https://github.com/alexgolec/schwab-py/tree/main)
- Flask

## Optional Requirements

These optional components allow this application to run as a production website.

- GUnicorn (optional)
- Apache / nginx (optional)

# Setting up your APP in Schwab

This is beyond the scope of this implementation.  Better to reference 'schwab-py' and their documents on how to create an APP in Schwab.  **[CLICK HERE](https://schwab-py.readthedocs.io/en/latest/getting-started.html)** for more information on getting started.

## Decisions made

### schwab-py

'schwab-py' was selected as the API abstraction library of choice after a few attempts to implement a standalone web application framework in other languages including:

- .php
- custom python backend code to perform OAuth actions
- golang (we almost looked at this, then said naaaah!)

The ***main*** reason 'schwab-py' was selected was for the ***ease of use*** for implementing OAuth Authentication into a custom built website (webapp).  Refreshing the OAuth bearer_token is tricky, and [schwab-py](https://github.com/alexgolec/schwab-py/tree/main) handles these details natively.

### Storing of secrets data

Another reason to use this reference design is because secrets data can be put into environment variables using Pythons 'dotenv' library.  The variables are imported into the webapp using native Python calls to get these datum from the operating system environment.  This is important so that no code written in this (or others) implementation has secrets data stored in the codebase.

## Notes

Notes go here.



## Disclaimer

Use of this code is your responsibility.  The examples provided are for learning only.  By using this codebase or any portions thereof you indemnify the authors from any damages or loss from using this codebase.  By proceeding to view, clone, or adopt any concepts from this code you make them your own.  The author claims no responsibility for any loss incurred from using this code base and/or reference design implementation.

This codebase may not be maintained or up-to-date with the latest [schwab-py](https://github.com/alexgolec/schwab-py/tree/main) implementations.  [schwab-py](https://github.com/alexgolec/schwab-py/tree/main) is on version 1.4.0 as of the origin of this document.

### Versions

#### Site1 LOGIN

##### Functionality

- OAuth login
- Quotes

This code uses sessions to store some information, specifically the account which is selected to use in API queires.

#### Site2 INTEGRATIONS

Functions from site 1:

- OAuth login
- Quotes

Additional functionality in site 2:

- Accounts
- Account Positions
- tbd

#### Site3 StreamClient

SchwabStream client implementation (stubbed out).  Require installation of [celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) and [redis](https://redis.io/)

## Links:

### Sister Channels:

<a href="https://www.twitch.tv/swizzlesticks2311" target="_blank" rel="noopener noreferrer">Twitch.TV</a>
<a href="https://www.youtube.com/@stockmarketswizzles" target="_blank" rel="noopener noreferrer">YouTube One</a>
<a href="https://www.youtube.com/channel/UCy_Y3dj3DIYcSJHEMR9MlSQ" target="_blank" rel="noopener noreferrer">YouTube Two</a>

### The ONE and ONLY: Coin Moulding (MUSIC)

<a href="https://www.youtube.com/watch?v=Mf09j3lxv4E" target="_blank" rel="noopener noreferrer">Watch on YouTube</a>


## Donate

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4XJC3BTYJ8ALG)

If you feel you benefit from this code repo consider a donation.

Button donation will read "Breaking Blackjack" ( a future endeavour ).  Thanks in advance.


## About This Project

This project came to us one day in a vision - to produce MUSIC from stock market data.  
From there, research and design was done, thousands of lines of code written, multiple  
websites stood up and torn down, databases installed, and python libraries written.  

From here: we are a group of out-of-work software developers doing what we love to do most: CODE.

This project is meant as a learning example of:

- programming in python
- practical application for automation
- automations to watch price movement in the stock market
- opportunities to learn the underlying mechanics of wave patterns in the stock market
- more ...

If you consider a donation the monies go to support our families and, well, just keeping our  
head above water.  Many developers do not pay for software they can obtain for free.  What  
they are really obtaining are TOOLS to accomplish a TASK they want to ACHIEVE.  Consider  
the value of this codebase to you, and please consider a donation to the cause.

No matter what, we will continue to code.  

YOUR SUPPORT IS APPRECIATED IN ADVANCE!

# Changelog

##### Version 1.1 (2025)
- Site 1 refactor and revisions
- backport some features
- Begin site 2 publication and refinement
- YouTube document for Login workflow

##### Version 1.0 (2024)
- Site 1 released
