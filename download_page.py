import requests, os, argparse

def save_page(url, file_name):
    os.makedirs("pages", exist_ok=True)
    res = requests.get(url)
    res.raise_for_status()
    with open(f'pages/{file_name}.html', 'wb') as file:
        for chunk in res.iter_content(100000):
            file.write(chunk)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Save a webpage to a local HTML file.")
    parser.add_argument("url", help="The URL of the webpage to download")
    parser.add_argument("file_name", help="The name of the file to save (without extension)")
    args = parser.parse_args()

    save_page(args.url, args.file_name)