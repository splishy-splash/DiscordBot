import requests
import re
from bs4 import BeautifulSoup


def parse_input(arg_list):
    movie = ''
    actor = ''
    character = ''

    # If we don't have -a or -m, we will assume the user is asking for a single movie or actor without comparing
    if (('-a' not in arg_list) and ('-m' not in arg_list)) or (('m' not in arg_list) and ('-c' not in arg_list)):
        return initial_query(' '.join(arg_list))

    # Checking for a specific actor in a specific movie
    # We check if they used -a or -m first, and grab the actor and movie into separate variables
    if '-a' in arg_list and '-m' in arg_list:
        if arg_list.index('-a') < arg_list.index('-m'):
            actor = ' '.join(arg_list[arg_list.index('-a') + 1: arg_list.index('-m')])
            movie = ' '.join(arg_list[arg_list.index('-m') + 1:])

        if arg_list.index('-a') > arg_list.index('-m'):
            movie = ' '.join(arg_list[arg_list.index('-m') + 1: arg_list.index('-a')])
            actor = ' '.join(arg_list[arg_list.index('-a') + 1:])

        # Doing the actual compare between our actor and the cast of the movie. Partial matches work!
        cast = cast_query(initial_query(movie))
        for member in cast:
            if member.find(actor.lower()) != -1:
                return "Totes in it!"
        return "Nope! Not in that one!"

    # Checking for a specific character in a movie or show
    if '-c' in arg_list and '-m' in arg_list:
        if arg_list.index('-c') < arg_list.index('-m'):
            character = ' '.join(arg_list[arg_list.index('-c') + 1: arg_list.index('-m')])
            movie = ' '.join(arg_list[arg_list.index('-m') + 1:])

        if arg_list.index('-c') > arg_list.index('-m'):
            movie = ' '.join(arg_list[arg_list.index('-m') + 1: arg_list.index('-c')])
            character = ' '.join(arg_list[arg_list.index('-c') + 1:])

        return character_query(initial_query(movie), character)


# Will do the equivalent of Google's 'I'm Feeling Lucky' for whatever term it is given and returns a URL to that page
def initial_query(term):
    # Build the initial request, but replace any spaces with '+'
    base_url = 'https://imdb.com/find?q='
    full_url = base_url + term.replace(" ", "+")

    # Request the page, give it to BeautifulSoup, and then parse the exact tag and href we need for the first result
    soup = BeautifulSoup(requests.get(full_url).text, 'lxml')
    match = soup.find('td', class_='result_text')
    return 'https://imdb.com/' + match.a['href']


# Will take result from initial_query() and return a full list of cast members
def cast_query(movie_url):
    cast_list = []

    # The page we need is base_url/fullcredits and then we parse it for the full cast list
    soup = BeautifulSoup(requests.get(movie_url + 'fullcredits').text, 'lxml')
    match = soup.find('table', class_='cast_list')

    # Remove the unwanted <td class=character> and <td class=ellipsis> tags
    for character in match.find_all('td', class_='character'):
        character.decompose()
    for ellipsis in match.find_all('td', class_='ellipsis'):
        ellipsis.decompose()

    # Only return filled items in our list, removing blanks
    for entry in match.find_all('td'):
        if entry.text.strip():
            cast_list.append(entry.text.lower().strip())
    return cast_list


def character_query(movie_url, person):
    character_list = {}

    # The page we need is base_url/fullcredits and then we parse it for the full cast list
    soup = BeautifulSoup(requests.get(movie_url + 'fullcredits').text, 'lxml')
    match = soup.find('table', class_='cast_list')

    # Get rid of elements we don't need
    for character in match.find_all('td', class_='primary_photo'):
        character.decompose()
    for ellipsis in match.find_all('td', class_='ellipsis'):
        ellipsis.decompose()
    for episodes in match.find_all('a', class_='toggle-episodes'):
        episodes.decompose()

    for entry in match.find_all('tr'):
        try:
            character = re.split("\n", (entry.select('td')[1].text.strip()))[0]
            actor = re.split("\n", (entry.select('td')[0].text.strip()))[0]
            character_list[character.lower()] = actor.lower()
        except:
            pass

    for i in character_list:
        if person in i:
            return character_list[i]

    return 'Not in it.'
