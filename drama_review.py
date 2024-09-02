from bs4 import BeautifulSoup
import requests
import pandas as pd

data = []

max_pages = 10700

for page_number in range(1, max_pages + 1):
    try:
        print(f"Scraping page {page_number} of {max_pages}...")

        url = f'https://mydramalist.com/reviews/shows?xlang=en-US&page={page_number}'
        source = requests.get(url)
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

        reviews = soup.find_all('div', class_='review')

        for review in reviews:
            try:
                title_tag = review.find('a', class_='text-primary')
                title = title_tag.text.strip() if title_tag else 'N/A'

                review_body = review.find('div', class_='review-body')
                review_text = review_body.text.strip() if review_body else 'N/A'

                overall_rating = review.find('div', class_='box pull-right text-sm m-a-sm')
                overall = overall_rating.text.strip() if overall_rating else 'N/A'

                data.append([title, overall, review_text])

                print(f"Title: {title}")
                print(f"Overall Rating: {overall}")
                print(f"Review: {review_text}\n")

            except Exception as e:
                print(f"Error processing review on page {page_number}: {e}")

    except Exception as e:
        print(f"Error on page {page_number}: {e}")

df = pd.DataFrame(data, columns=['Movie Name', 'Overall Rating', 'Review'])

df.to_csv('MDL_Drama_Reviews.csv', index=False)
