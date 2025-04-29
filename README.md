# TripAdvisor Hotel Review Scraper

Hey! This is a little Python script I put together to help you grab reviews from TripAdvisor hotel pages. It also does a quick sentiment check on each review, then saves everything to a CSV file. Super handy if you want to mess around with the data in Excel or Power BI.

## What does it do?
- Pulls reviews from as many TripAdvisor hotel URLs as you want. Just paste them into a list.
- Goes through several pages of reviews for each hotel (you can set how many pages to scrape).
- Runs a simple sentiment check (positive, negative, or neutral) using NLTK's VADER tool.
- Dumps all the results into a file called tripadvisor_reviews_all_hotels.csv in the same folder.

## How to get started

1. Make sure you have Python 3.7 or newer on your computer.
2. Install the libraries you need. Open a terminal in this folder and run:
   pip install -r requirements.txt
   (You'll need requests, beautifulsoup4, pandas, and nltk.)
3. Open up scrape_tripadvisor.py in your editor.
4. Scroll to the bottom and find the start_urls list. Paste in all the TripAdvisor hotel review URLs you want to scrape.
5. If you run the script and it says "No reviews found...", TripAdvisor probably changed their website again. Open a review page in your browser, right-click a review, hit Inspect, and look for the class name on the span tag that holds the review text. Copy that class and update the REVIEW_BLOCK_CLASS variable in the script.
6. To run the script, just do:
   python scrape_tripadvisor.py
7. When it's done, you'll have a CSV file with all your reviews. Open it up in Excel or Power BI, and you're good to go.

## What's in the CSV file?
Here's what each column means:
- Hotel Name: Whatever name was scraped from the page. Sometimes TripAdvisor adds extra stuff, so you might want to clean this up in Excel.
- Page: Which review page this review was found on.
- Review Number: Just a running count for the reviews.
- Rating: Not grabbed by default—it's set to None unless you update the script to pull it in.
- Review Text: The actual review.
- Sentiment: What the script thinks about the review (positive, negative, or neutral).

## Tips and troubleshooting
- If you get no reviews, double check the review block selector as described above.
- Want more info, like ratings, reviewer names, or dates? You'll need to inspect the page and tweak the script to grab those fields.
- Need more pages? Change the max_pages number at the bottom of the script.
- Want to scrape more hotels? Just add more URLs to the start_urls list.

## Example
Here's how you set up your URLs and run the scraper:

start_urls = [
    "https://www.tripadvisor.com/Hotel_Review-g1175545-d14184436-Reviews-Domes_Miramare_A_Luxury_Collection_Resort-Moraitika_Corfu_Ionian_Islands.html",
    "https://www.tripadvisor.in/Hotel_Review-g60763-d7816364-Reviews-Executive_Hotel_Le_Soleil_New_York-New_York_City_New_York.html",
    # ...add more URLs here
]
scrape_tripadvisor_reviews_multiple(start_urls, max_pages=5, output_file="tripadvisor_reviews_all_hotels.csv")

## Just a quick note
This is for personal or school projects. Please don't use it to scrape tons of data or for commercial stuff. TripAdvisor might block you if you go overboard.

If you run into any problems or have questions, feel free to ask for help. Good luck and happy scraping!
