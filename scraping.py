from bs4 import BeautifulSoup
import requests
import openpyxl


excel = openpyxl.workbook()
print(excel.sheetnames)
sheet = excel.active
sheet.title = 'Top Rated Movies in MDL'
print(excel.sheetnames)
sheet.append(['Movie Rank', 'Movie Name', 'Original Language - Year of Release', 'Overview', 'MDL Rating'])

max_pages = 260
for page_number in range(1, max_pages + 1):
    try:
        url = f'https://mydramalist.com/movies/top?page={page_number}'
        source = requests.get(url)
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

        movies = soup.find(class_='m-t nav-active-border b-primary').find_all(class_='col-xs-9 row-cell content')

        for movie in movies:
            title = movie.find('h6', class_='text-primary title').a.text
            rank = movie.find(class_='ranking pull-right').span.text
            year = movie.find('span', class_='text-muted').text
            MDL_rating = movie.find(class_='p-l-xs score').text
            
            
            p_tags = movie.find_all('p')
    
            
            if len(p_tags) > 1:
                Overview = p_tags[1].text  
            else:
                Overview = '' 
            
            #print(rank, title, year, Overview, MDL_rating)
            sheet.append([rank, title, year, Overview, MDL_rating])

    except Exception as e:
        print(f"Error on page {page_number}: {e}")


workbook.save("MDL_Top_Movies_Rating.xlsx")
