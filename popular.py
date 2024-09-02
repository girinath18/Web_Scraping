import requests
from bs4 import BeautifulSoup
import csv


with open("MDL_Most_Popular_Drama.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow(['Most Popular Drama', 'Drama Rank', 'Drama Name', 'Original Language - Year of Release', 'Overview', 'Episodes', 'MDL Rating'])

    popular_movies_counter = 1
    max_pages = 260

    for page_number in range(1, max_pages + 1):
        try:
            url = f'https://mydramalist.com/shows/popular?page={page_number}'
            source = requests.get(url)
            source.raise_for_status()

            soup = BeautifulSoup(source.text, 'html.parser')

            movies = soup.find(class_='m-t nav-active-border b-primary').find_all(class_='col-xs-9 row-cell content')

            for movie in movies:
                title = movie.find('h6', class_='text-primary title').a.text.strip()
                rank = movie.find(class_='ranking pull-right').span.text.strip()
                year_and_episodes = movie.find('span', class_='text-muted').text.strip()
                MDL_rating = movie.find(class_='p-l-xs score').text.strip()
                
               
                p_tags = movie.find_all('p')
                overview = p_tags[1].text.strip() if len(p_tags) > 1 else "N/A"

                if ',' in year_and_episodes:
                    year, episodes = [part.strip() for part in year_and_episodes.split(',', 2)]
                else:
                    year = year_and_episodes
                    episodes = "N/A"
                
                writer.writerow([popular_movies_counter, rank, title, year, overview, episodes, MDL_rating])
                
                
                popular_movies_counter += 1

        except Exception as e:
            print(f"Error on page {page_number}: {e}")
