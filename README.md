# schwab-py-webframework-reference-design
Intended reference design for a practical example of using [schwab-py](https://github.com/alexgolec/schwab-py/tree/main) in a working web application (web framework).  

***As a note:*** This codebase not officially associated with 'schwab-py'.  

***Disclaimer:*** We claim no responsibility for keeping up-to-date with changes in 'schwab-py' in this reference design.  However, the intent is to demonstrate in simple terms how to "create a working web application" using the 'schwab-py' API abstraction library which is built in Python.

## Donate

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4XJC3BTYJ8ALG)

If you feel you benefit from this code repo consider a donation.

Button donation will read "Breaking Blackjack" ( a future endeavour ).  Thanks in advance.

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

# Changelog

##### Version 1.1 (2025)
- Site 1 refactor and revisions
- backport some features
- Begin site 2 publication and refinement
- YouTube document for Login workflow

##### Version 1.0 (2024)
- Site 1 released
