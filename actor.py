from bs4 import BeautifulSoup
import requests
import csv

# Open the CSV file for writing
with open('MDL_Actors_Rating.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
        
    writer.writerow(['Actor Names', 'Country', 'Actor Details', 'Likes'])
    
    max_pages = 250
    for page_number in range(1, max_pages + 1):
        try:
            url = f'https://mydramalist.com/people/top?page={page_number}'
            source = requests.get(url)
            source.raise_for_status()

            
            soup = BeautifulSoup(source.text, 'html.parser')

            
            movies = soup.find_all('div', class_='box')

            
            for movie in movies:
                try:

                    print(f"Scraping page {page_number} of {max_pages}...")
                    
                    actor_tag = movie.find('h6', class_='text-primary title')
                    if actor_tag and actor_tag.a:
                        actor = actor_tag.a.text.strip()
                    else:
                        actor = 'N/A'
                    
                    
                    country_tag = movie.find('div', class_='text-muted')
                    if country_tag:
                        country_span = country_tag.find('span', class_='spacer')
                        country = country_span.text.strip() if country_span else 'N/A'
                    else:
                        country = 'N/A'
                    
                    # Extract actor details (Check if element exists)
                    details_tag = movie.find('p')
                    actor_details = details_tag.text.strip() if details_tag else 'N/A'
                    
                    
                    likes_tag = movie.find('span', class_='like-cntb')
                    likes = likes_tag.text.strip() if likes_tag else 'N/A'

                    
                    writer.writerow([actor, country, actor_details, likes])

                    print(actor, country, actor_details, likes)

                except AttributeError as e:
                    print(f"Error processing movie on page {page_number}: {e}")
                    continue

        except Exception as e:
            print(f"Error on page {page_number}: {e}")
