from bs4 import BeautifulSoup
import requests
import openpyxl

# Create a new Excel workbook
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = 'MDL_Newest_Movies'

# Print the sheet names to verify
print(workbook.sheetnames)

# Add headers to the Excel sheet
sheet.append(['Movie Name', 'Original Language - Year of Release', 'Overview', 'MDL Rating'])

# Set the maximum number of pages to scrape
max_pages = 260
for page_number in range(1, max_pages + 1):
    try:
        # Construct the URL for each page
        url = f'https://mydramalist.com/movies/newest?page={page_number}'
        source = requests.get(url)
        source.raise_for_status()

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(source.text, 'html.parser')

        # Find the movies on the page
        movies = soup.find(class_='m-t nav-active-border b-primary').find_all(class_='col-xs-9 row-cell content')

        for movie in movies:
            title = movie.find('h6', class_='text-primary title').a.text
            year = movie.find('span', class_='text-muted').text
            MDL_rating = movie.find(class_='p-l-xs score').text
            
            # Find the overview, if it exists
            p_tags = movie.find_all('p')
            if len(p_tags) > 1:
                Overview = p_tags[1].text  
            else:
                Overview = ''
            
            # Append the data to the Excel sheet
            sheet.append([title, year, Overview, MDL_rating])

    except Exception as e:
        print(f"Error on page {page_number}: {e}")

# Save the workbook to a file
workbook.save("MDL_Newest_Movies.xlsx")
