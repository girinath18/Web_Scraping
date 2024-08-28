from bs4 import BeautifulSoup
import requests
import openpyxl


workbook = openpyxl.Workbook()
sheet = workbook.active


sheet.append(['Most Popular', 'Movie Rank', 'Movie Name', 'Original Language - Year of Release', 'MDL Rating'])


popular_movies_counter = 1


max_pages = 260

for page_number in range(1, max_pages + 1):
    try:
        url = f'https://mydramalist.com/movies/popular?page={page_number}'
        source = requests.get(url)
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

        movies = soup.find(class_='m-t nav-active-border b-primary').find_all(class_='col-xs-9 row-cell content')

        for movie in movies:
            title = movie.find('h6', class_='text-primary title').a.text
            rank = movie.find(class_='ranking pull-right').span.text
            year = movie.find('span', class_='text-muted').text
            MDL_rating = movie.find(class_='p-l-xs score').text
            
            
            sheet.append([popular_movies_counter, rank, title, year, MDL_rating])
            
            # Increment the counter
            popular_movies_counter += 1

    except Exception as e:
        print(f"Error on page {page_number}: {e}")

# Save the workbook
workbook.save("MDL's Most Popular Movies.xlsx")
