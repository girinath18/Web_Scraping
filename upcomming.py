from bs4 import BeautifulSoup
import requests
import csv


with open('MDL_Upcomming_Drama.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    
    writer.writerow(['Web Series Name', 'Original Language - Year of Release', 'Episodes', 'Overview'])

    max_pages = 8

    for page_number in range(1, max_pages + 1):
        try:
            url = f'https://mydramalist.com/shows/upcoming?page={page_number}'
            source = requests.get(url)
            source.raise_for_status()

            soup = BeautifulSoup(source.text, 'html.parser')

            movies = soup.find_all('div', class_='box')

            for movie in movies:
                try:
                    title = movie.find('h6', class_='text-primary title').a.text.strip()
                    rank = movie.find(class_='ranking pull-right').span.text.strip()
                    year_and_episodes = movie.find('span', class_='text-muted').text.strip()
                    
                    # Split the string by comma to separate year and episodes
                    if ',' in year_and_episodes:
                        year, episodes = [part.strip() for part in year_and_episodes.split(',', 1)]
                    else:
                        year = year_and_episodes
                        episodes = "N/A"
                    
                    #MDL_rating = movie.find(class_='p-l-xs score').text.strip()
                    
                    # Find the correct <p> tag for the overview
                    overview_tag = movie.find_all('p')
                    if len(overview_tag) > 1:
                        overview = overview_tag[1].text.strip()  
                    else:
                        overview = "Overview not available"
                  
                    print(title, year, episodes, overview)
                    
                    
                    writer.writerow([title, year, episodes, overview])

                except AttributeError as e:
                    print(f"Error processing movie on page {page_number}: {e}")
                    continue

        except Exception as e:
            print(f"Error on page {page_number}: {e}")
