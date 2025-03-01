from googlesearch import search
import requests
import re
from bs4 import BeautifulSoup
import os
import wikipedia

intro = """# Chess Openings: The Grand Entrance to Victory

Ah, chess—the ultimate battle of minds, where kings cower, queens dominate, and pawns dream of becoming something greater. A game so deep that even after centuries of study, grandmasters continue to explore its endless complexities, uncovering new ideas move by move.

But before you can checkmate your opponent in a blaze of glory, you must first navigate the treacherous waters of **the opening**. Chess openings are like entrances at a royal ball—walk in with confidence, and you might just become the star of the evening. Stumble in clueless, and you’ll be swept off the board before you can say *"en passant."*

Here, you'll find a collection of chess openings, each with its own style, strategy, and historical drama. Whether you prefer the elegance of the Italian Game, the sheer chaos of the King's Gambit, or the sinister depths of the Sicilian Defense, there’s an opening here for you.

So grab your coffee, adjust your imaginary monocle, and dive into the fascinating world of chess openings. Who knows? With the right moves, you might just become the next legend of the 64 squares!

For a full list of openings, check out [this guide](openings.md)."""

url = 'https://www.thechesswebsite.com/chess-openings/'
# Get the soup of the page
def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code != 200:
        print('Status code:', response.status_code)
        print('Failed to get the page:', url)
        return None
    return soup

# Get data from opening
def strip_opening(opening):
    name = opening.find("h5")
    link = opening.get("href")
    img_tag = opening.find("img")
    img_src = img_tag["src"] if img_tag else "Brak obrazka"
    accesibility = opening.find("span")
    return{
        "name": name.text.strip(),
        "link": link,
        "img_src": img_src,
        "accesibility": 0 if accesibility else 1
        }

def get_openings():
    soup = get_soup(url)
    assert soup is not None

    # Find the container with the openings
    container_list = []
    outer_div= soup.find_all("div", class_='elementor-widget-container')
    for elem in outer_div:
        if elem.find("div", id='cb-container') is not None:
            container_list.append(elem.find("div", id='cb-container'))

    # Desired container (checked epmirically)
    container = container_list[1]
    openings = container.find_all("a")

    ret_list = []
    for opening in openings:
        ret_list.append(strip_opening(opening))

    return ret_list

def write_openings_to_file(openings):
    with open("openings.md", "w") as file:
        file.write("# List of chess openings \n\n")
        for opening in openings:
            op_file = "wiki_info/" + normalize(opening["name"]) + ".md"
            #create directory if not exists
            os.makedirs(os.path.dirname(op_file), exist_ok=True)
            with open(op_file, "w") as op:
                op.write("# " + opening["name"] + "\n\n")
                op.write("![Opening image](" + opening["img_src"] + ")\n\n")
                op.write(get_wikipedia_info(opening))
            file.write("- [" + opening["name"] + "](wiki_info/" + normalize(opening["name"]) + ".md)\n")

def get_wikipedia_info(opening):
    query = opening["name"]
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query)
        summary = "\n\n".join(summary.split("\n"))
    except wikipedia.exceptions.PageError as e:
        summary = ""
    return summary

def normalize(name):
    name = name.lower()  # Zamienia wszystkie litery na małe
    name = re.sub(r"[^a-z0-9]", "", name)  # Usuwa znaki specjalne i spacje
    return name

def intro_page():
    with open("intro.md", "w") as file:
        file.write(intro)


intro_page()
write_openings_to_file(get_openings())
