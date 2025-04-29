import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def get_sentiment(text, sid):
    scores = sid.polarity_scores(str(text))
    compound = scores['compound']
    if compound >= 0.05:
        return 'positive'
    elif compound <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def scrape_tripadvisor_reviews_multiple(start_urls, max_pages=5, output_file="tripadvisor_reviews_all_hotels.csv"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    all_reviews_data = []
    sid = SentimentIntensityAnalyzer()

    # Update this selector if needed!
    REVIEW_BLOCK_CLASS = 'orRIx Ci _a C'  # Updated to match the review text span

    for start_url in start_urls:
        current_page = 0
        hotel_name = ''
        for page in range(1, max_pages + 1):
            url = f"{start_url[:-5]}-or{(page-1)*10}{start_url[-5:]}"
            print(f"Fetching page {page} for hotel: {url}")
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to retrieve the page for {url}. Status code: {response.status_code}")
                break
            soup = BeautifulSoup(response.content, 'html.parser')
            if page == 1:
                hotel_name_tag = soup.find('h1')
                hotel_name = hotel_name_tag.get_text(strip=True) if hotel_name_tag else "Hotel Name Not Found"
                print(f"Hotel Name: {hotel_name}")

            # Find review text spans (update class if needed)
            review_spans = soup.find_all('span', class_=REVIEW_BLOCK_CLASS)
            if not review_spans:
                print(f"No reviews found on this page for hotel {hotel_name}. Try updating REVIEW_BLOCK_CLASS.")
                break
            for idx, span in enumerate(review_spans, 1):
                review_text = span.get_text(strip=True)
                rating = None  # Rating extraction not implemented in this step
                sentiment = get_sentiment(review_text, sid)
                all_reviews_data.append({
                    "Hotel Name": hotel_name,
                    "Page": page,
                    "Review Number": idx + (current_page * len(review_spans)),
                    "Rating": rating,
                    "Review Text": review_text,
                    "Sentiment": sentiment
                })
            current_page += 1
            time.sleep(2)

    if all_reviews_data:
        df = pd.DataFrame(all_reviews_data)
        df.to_csv(output_file, index=False)
        print(f"All reviews successfully saved to {output_file}")
    else:
        print("No reviews were collected. No file created.")

# Example usage:
start_urls = [
    "https://www.tripadvisor.com/Hotel_Review-g1175545-d14184436-Reviews-Domes_Miramare_A_Luxury_Collection_Resort-Moraitika_Corfu_Ionian_Islands.html",
    "https://www.tripadvisor.in/Hotel_Review-g60763-d7816364-Reviews-Executive_Hotel_Le_Soleil_New_York-New_York_City_New_York.html",
    "https://www.tripadvisor.in/Hotel_Review-g60763-d113317-Reviews-Casablanca_Hotel_By_Library_Hotel_Collection-New_York_City_New_York.html",
    "https://www.tripadvisor.in/Hotel_Review-g60763-d10679074-Reviews-Luma_Hotel_Time_Square-New_York_City_New_York.html"
]
scrape_tripadvisor_reviews_multiple(start_urls, max_pages=5, output_file="tripadvisor_reviews_all_hotels.csv")
