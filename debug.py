from save_tournaments import load_html, parse_tournament_info, parse_tournament_results

if __name__ == '__main__':
    soup = load_html("pages/tournaments/01.html")
    tournament_info = parse_tournament_info(soup)
    tournament_results = parse_tournament_results(soup)
    print(tournament_info)
    print(tournament_results)
