import argparse

import bs4
import psycopg
import uuid
from dateutil import parser

DBCONN = "dbname=riichi_two user=postgres password=admin"

def load_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return bs4.BeautifulSoup(file, 'html.parser')

def __parse_tournament_info_cell(cell):
    return cell.find_all('td')[1].get_text(strip=True).replace('\n', '')

def __parse_tournament_info_date(cell):
    date = __parse_tournament_info_cell(cell)
    if '-' in date:
        cleaned_date = date.split(' ')[0].split('-')[0] + ' ' + date.split(' ')[
            1].replace('.', '') + ' ' + date.split(' ')[2]
        return parser.parse(cleaned_date)
    else:
        return parser.parse(date)

def __get_country_from_img_link(parent):
    return (img := parent.find('img')) and img.attrs['src'].split('/')[-1].split('.')[0] or None

def parse_tournament_info(soup):
    table = soup.find('table')
    rows = table.find_all('tr')
    return {
        'number': __parse_tournament_info_cell(rows[1]),
        'name': __parse_tournament_info_cell(rows[2]),
        'place': __parse_tournament_info_cell(rows[3]).replace('(see National Stats)',''),
        'country': __get_country_from_img_link(rows[3].find_all('td')[1]),
        'date': __parse_tournament_info_date(rows[4]),
        'players': __parse_tournament_info_cell(rows[5]),
        'mers': __parse_tournament_info_cell(rows[6]),
        'rules': __parse_tournament_info_cell(rows[7])
    }

def parse_tournament_results(soup):
    score_divs = soup.select_one('.TCTT_lignes').find_all('div')
    data = []
    # skip the headers at index 0
    for row in score_divs[1:]:
        row_ps = row.find_all('p')
        # row_ps[0] is position
        last_name = row_ps[2].get_text(strip=True).casefold()
        first_name = row_ps[3].get_text(strip=True).casefold()
        if first_name == "-" and last_name == "-":
            last_name = str(uuid.uuid4())
        # remove empty values
        ema_id = row_ps[1].get_text(strip=True)
        if ema_id == "-":
            ema_id = None
        data.append({
            'ema_id': ema_id,
            'last_name': last_name,
            'first_name': first_name,
            'country': __get_country_from_img_link(row_ps[4]),
            'score': row_ps[6].get_text(strip=True)
        })
    return data

def get_player_id(cur, ema_id, first_name, last_name):
    if ema_id:
        cur.execute(
            "select id from players where ema_id = %s;",
            [ema_id])
        player = cur.fetchone()
        if player:
            return player[0]

    cur.execute(
        "select id from players where first_name = %s and last_name = %s",
        (first_name, last_name)
    )
    player = cur.fetchone()
    if player:
        return player[0]
    return None

def create_player(cur, first_name, last_name, country, ema_id):
    cur.execute(
        """insert into players (ema_id, first_name, last_name, country) 
        values (%s, %s, %s, %s) returning id""",
        (ema_id, first_name, last_name, country))
    return cur.fetchone()[0]

def create_tournament(cur, tournament_info):
    cur.execute(
        """insert into tournaments (number, name, place, country, date, players, mers, rules) 
        values (%s, %s, %s, %s, %s, %s, %s, %s) returning id""",
        (tournament_info['number'], tournament_info['name'], tournament_info['place'],
         tournament_info['country'], tournament_info['date'],
         tournament_info['players'], tournament_info['mers'], tournament_info['rules'])
    )
    return cur.fetchone()[0]

def insert_tournament_results(cur, tournament_id, player_scores):
    for player in player_scores:
        ema_id = player['ema_id']
        last_name = player['last_name']
        first_name = player['first_name']
        country = player['country']
        score = player['score']
        if score == "-" or score == "N/A":
            continue
        player_id = get_player_id(cur, ema_id, first_name, last_name)
        if player_id is None:
            player_id = create_player(cur, first_name, last_name, country, ema_id)
        cur.execute("""INSERT INTO tournament_results (tournament_id, player_id, score) 
                            VALUES (%s, %s, %s)""",
                    (tournament_id, player_id, score)
                    )

def save_tournament_page_to_db(file_path):
    soup = load_html(file_path)
    tournament_info = parse_tournament_info(soup)
    data = parse_tournament_results(soup)

    with psycopg.connect(DBCONN) as conn:
        with conn.cursor() as cur:
            tournament_id = create_tournament(cur, tournament_info)
            insert_tournament_results(cur, tournament_id, data)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Download tournament ranking pages.")
    argparser.add_argument("start", type=int, help="Starting tournament number")
    argparser.add_argument("end", type=int, help="Ending tournament number")
    args = argparser.parse_args()
    for number in range(args.start, args.end):
        print(f"Scraping tournament page {number}")
        save_tournament_page_to_db(f'pages/tournaments/{str(number).zfill(2)}.html')