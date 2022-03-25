# CRICK :cricket_game:

An attempt at a simple _hobby-project_ in hope to improve my python-skills.

### Wishlist

- using industry best-practices with python dev (venv, black, pylint, mypy, oop concepts, unit-tests etc) while building a cricket match simulator
- build GUI for registering teams, display scoresheets
- build CLI for registering teams and other admin stuffs
- build API for getting match stats
- web-scraping for getting a realistic dataset
- build a data pipeline for processing match scorecards
- build a dashboard out of processed data
 

### How to use?

- Clone the repo and then from the repo root, invoke -
  ```
  python -m match.match -f ODI   # -f options can be one of [T20, ODI, Test]
  ```
  This will play-out a simulation and prints the match scorecards - _batting, bowling, FOW_ and _over-by-over_ cards to console and also saves them as a file under `/simulations`
  
  batting card
  
  ![sample_batting_sheet](https://user-images.githubusercontent.com/23091121/160048144-9e060a46-b1a5-4a0f-a563-b32763367809.png)
  
  bowling card
  
  ![sample_bowling_sheet](https://user-images.githubusercontent.com/23091121/160048221-52841e31-91bc-47e2-b263-a23c7c1a42ca.png)

  fow
  
  ![sample_fow](https://user-images.githubusercontent.com/23091121/160048259-7a64a6b5-ae29-4d6a-8e37-7ea3fb9749e8.png)

  
