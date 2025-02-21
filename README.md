# 🀄 EMA Tournament Scraper

Save a bunch of tournament pages locally and then scrape them for data.

## 📥 Installation

### 1️⃣ Clone the Repository
```shell
git clone https://github.com/ea-ncu/ema-riichi-scraper
cd ema-riichi-scraper
```
### 2️⃣ Install Dependencies
Ensure you have Python installed (>=3.7). Then install required packages:
```shell
pip install -r requirements.txt
```
### 3️⃣ Setup PostgreSQL Database
Ensure PostgreSQL is running and create a database:
```postgresql
create database riichi;
```
Run the commands found in `postgres/init.sql` 

If needed, add a `DBCONN` environment variable or modify the default value found in `save_tournaments.py`

## 🚀 Usage
### 1️⃣ Download Tournament Pages

Download tournament pages for offline use/scraping:
```shell
python download_tournaments.py 1 365
```
There is some additional code to fix some files so that the date can be parsed correctly.
### 2️⃣ Parse and Store Tournament Data
To extract data from downloaded pages and store it in PostgreSQL:
```shell
python save_tournaments.py 1 365
```
