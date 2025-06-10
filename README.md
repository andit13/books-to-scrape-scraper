# Web Scraper for books.toscrape.com

This project is a Python web scraper designed to extract book information from the demo website books.toscrape.com. The collected data includes the title, price, rating, availability, and URL of each book, and is saved in CSV format.

**Objective:** To demonstrate web scraping skills, including page navigation, structured data extraction, and data persistence.

## Features

* Navigates through all 50 catalogue pages.
* Extracts `title`, `price` (as a numerical value), `rating` (converted to a 5-point scale), and `availability` (`In stock` / `Out`).
* Generates the full `URL` for each book.
* Saves the data to `books.csv` (UTF-8 encoded, `;` delimiter).
* Includes validation checks for 1000 rows, no duplicate URLs, and a positive average price.

## Technologies Used

* Python 3.x
* `requests` (for HTTP requests)
* `BeautifulSoup4` (for HTML parsing)
* `re` (for regular expressions, specifically for price extraction)
* `csv` (for working with CSV files)

## How to Run Locally

To get a local copy up and running, follow these simple steps.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/books-to-scrape-scraper.git](https://github.com/YOUR_USERNAME/books-to-scrape-scraper.git)
    cd books-to-scrape-scraper
    ```
    (Replace `YOUR_USERNAME` with your actual GitHub username)

2.  **Install dependencies:**
    ```bash
    pip install requests beautifulsoup4
    ```

3.  **Run the scraper:**
    ```bash
    python scraper.py
    ```
    After the script finishes, a `books.csv` file will be created in the same directory.

---

## Contact

* **Email:** and.od.it13@gmail.com

