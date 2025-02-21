import argparse
import os

from download_page import save_page

def save_tournament_pages(start, end):
    for number in range(start, end):
        key = str(number).zfill(2) if number < 100 else str(number)
        url = f'http://mahjong-europe.org/ranking/Tournament/TR_RCR_{key}.html'
        print(f'Saving page for URL {url}')
        save_page(url, f'tournaments/{key}')

def __fix_tournament_file(file_name, search_text, replace_text):
    file_path = f'pages/tournaments/{file_name}.html'
    if os.path.exists(file_path):
        # due to one file containing a funky character, we ignore errors to be able to fix it
        with open(file_path, 'r', errors="ignore") as file:
            data = file.read()
            data = data.replace(search_text, replace_text)
        with open(file_path, 'w') as file:
            file.write(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download tournament ranking pages.")
    parser.add_argument("start", type=int, help="Starting tournament number")
    parser.add_argument("end", type=int, help="Ending tournament number")
    args = parser.parse_args()

    save_tournament_pages(args.start, args.end)
    # some files need some data cleaned
    __fix_tournament_file("52", "17-mars-13", "17 Mar 2013")
    __fix_tournament_file("94", "31 Jan. 1 Feb 2015", "31 Jan 2015")
    __fix_tournament_file("224", "23-24 Mars 2019", "23 Mar 2019")
    __fix_tournament_file("227", "13-14 Apr.2019", "13 Apr 2019")
    __fix_tournament_file("228", "13-14 Apr.2019", "13 Apr 2019")
    __fix_tournament_file("242", "2021 Jul. 2019", "20 Jul 2019")
    __fix_tournament_file("265", "18 Janv. 2020", "18 Jan 2020")
    __fix_tournament_file("306", "16 - 17 SEP 2023","16 Sep 2023")