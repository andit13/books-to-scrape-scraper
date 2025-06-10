import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin

class BooksScraper:
    def __init__(self):
        self.base_url = "https://books.toscrape.com"
        self.books_data = []
        self.session = requests.Session()
        # Add headers to mimic a regular browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def convert_rating_to_number(self, rating_class):
        """Convert text rating to numerical value"""
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }

        for word, number in rating_map.items():
            if word in rating_class:
                return number
        return 0

    def clean_price(self, price_text):
        """Extract numerical price value"""
        # Remove currency symbol and convert to float
        price_clean = re.sub(r'[£$€]', '', price_text.strip())
        try:
            return float(price_clean)
        except ValueError:
            return 0.0

    def scrape_page(self, page_url):
        """Parse a single catalog page"""
        print(f"Scraping page: {page_url}")

        try:
            response = self.session.get(page_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all book cards
            book_articles = soup.find_all('article', class_='product_pod')

            for article in book_articles:
                try:
                    # Book title
                    title_element = article.find('h3').find('a')
                    title = title_element.get('title', title_element.get_text(strip=True))

                    # Book URL
                    book_url = urljoin(self.base_url + '/catalogue/', title_element.get('href'))

                    # Price
                    price_element = article.find('p', class_='price_color')
                    price = self.clean_price(price_element.get_text()) if price_element else 0.0

                    # Rating
                    rating_element = article.find('p', class_=re.compile(r'star-rating'))
                    rating_classes = rating_element.get('class') if rating_element else []
                    rating = 0
                    for cls in rating_classes:
                        if cls in ['One', 'Two', 'Three', 'Four', 'Five']:
                            rating = self.convert_rating_to_number(cls)
                            break

                    # Availability
                    availability_element = article.find('p', class_='instock availability')
                    if availability_element:
                        availability_text = availability_element.get_text(strip=True)
                        availability = "In stock" if "In stock" in availability_text else "Out of stock"
                    else:
                        availability = "Unknown"

                    # Add book data
                    book_data = {
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'availability': availability,
                        'url': book_url
                    }

                    self.books_data.append(book_data)

                except Exception as e:
                    print(f"Error parsing book: {e}")
                    continue

            return len(book_articles)

        except Exception as e:
            print(f"Error loading page {page_url}: {e}")
            return 0

    def scrape_all_pages(self):
        """Parse all catalog pages"""
        print("Starting to scrape all pages...")

        # First page
        first_page_url = f"{self.base_url}/catalogue/page-1.html"
        books_count = self.scrape_page(first_page_url)

        if books_count == 0:
            print("No books found on first page")
            return

        # Parse remaining pages (2-50)
        for page_num in range(2, 51):
            page_url = f"{self.base_url}/catalogue/page-{page_num}.html"

            books_on_page = self.scrape_page(page_url)

            # If page has no books, we might have reached the end
            if books_on_page == 0:
                print(f"Page {page_num} is empty, possibly reached catalog end")
                break

            # Small delay between requests
            time.sleep(0.5)

        print(f"Total books scraped: {len(self.books_data)}")

    def save_to_csv(self, filename='books.csv'):
        """Save data to CSV file"""
        if not self.books_data:
            print("No data to save")
            return

        print(f"Saving data to {filename}...")

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'price', 'rating', 'availability', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            # Write headers
            writer.writeheader()

            # Write book data
            for book in self.books_data:
                writer.writerow(book)

        print(f"Data saved to {filename}")

    def validate_data(self):
        """Validate scraped data quality"""
        print("\n=== DATA VALIDATION ===")

        total_books = len(self.books_data)
        print(f"Total books: {total_books}")

        # Check for URL duplicates
        unique_urls = set(book['url'] for book in self.books_data)
        duplicates = total_books - len(unique_urls)
        print(f"Unique URLs: {len(unique_urls)}")
        if duplicates > 0:
            print(f"⚠️  Found duplicates: {duplicates}")
        else:
            print("✅ No duplicates found")

        # Average price
        prices = [book['price'] for book in self.books_data if book['price'] > 0]
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"Average price: £{avg_price:.2f}")
            if avg_price > 0:
                print("✅ Average price is above 0")
            else:
                print("⚠️  Average price is 0")

        # Check expected count (~1000)
        if 900 <= total_books <= 1100:
            print("✅ Book count within expected range")
        else:
            print(f"⚠️  Book count ({total_books}) not as expected (~1000)")

        # Rating statistics
        ratings = [book['rating'] for book in self.books_data]
        print(f"Ratings: 1★:{ratings.count(1)}, 2★:{ratings.count(2)}, 3★:{ratings.count(3)}, 4★:{ratings.count(4)}, 5★:{ratings.count(5)}")

def main():
    """Main function"""
    scraper = BooksScraper()

    try:
        # Scrape all pages
        scraper.scrape_all_pages()

        # Validate data
        scraper.validate_data()

        # Save to CSV
        scraper.save_to_csv('books.csv')

        print("\n✅ Scraping completed successfully!")

    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Execution error: {e}")

# Run the scraper
main()