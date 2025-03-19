# Carma Scraper

This project is a Python-based web scraper that extracts product details from the Carma website. Proof of concept for DCO to scrape web data for a live build. It downloads the top 3 product images and extracts details such as title, variant, distance, transmission, price, and repayment information. The scraped data is saved in a JSON file, and images are organized in an `img` folder.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running (for containerized usage).
- Git (if you plan to clone this repository).
- (Optional) Python 3 if you wish to run the project locally without Docker.

## How to Run the Project

### Option 1: Using Docker

1. **Clone the Repository:**

    git clone https://github.com/mt-bradley/carma-scraper.git
    cd carma-scraper

2. **Build the Docker Image:**

    docker build -t carma-scraper .

3. **Run the Docker Container:**

   To simply run the container:

    docker run --rm carma-scraper

   To persist the downloaded images on your host machine, mount the `img` folder:

    docker run --rm -v "$(pwd)/img:/app/img" carma-scraper

4. **(Optional) Load a Prebuilt Image:**

   If you're sharing the provided Docker image archive, load it with:

    docker load -i carma-scraper.tar
    docker run --rm carma-scraper

### Option 2: Running Locally Without Docker

1. **Set Up a Virtual Environment:**

    python3 -m venv venv
    source venv/bin/activate

2. **Install Dependencies:**

    pip install -r requirements.txt

3. **Run the Scraper:**

    python main.py

## Customization

Feel free to modify the scraping logic in `main.py` as needed. For example, you can adjust the number of product cards scraped or change the data extraction process based on your requirements.

## License

This project is licensed under the [MIT License](LICENSE).
