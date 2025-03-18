import requests
from bs4 import BeautifulSoup
import json
import os

def download_image(image_url, filename):
    """
    Download the image from image_url and save it to a file inside the 'img' folder.
    """
    # Make an img folder
    img_folder = "img"
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    
    # Create the full file path within the img folder
    file_path = os.path.join(img_folder, filename)
    
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded image: {file_path}")
    except Exception as e:
        print(f"Error downloading image {image_url}: {e}")

def scrape_carma_cards(url, top_n=3):
    """
    1. Scrape the Carma Au website for the top_n product cards.
    2. Extracts the image, title, variant, distance, transmission, price, and repayment info.
    3. Downloads the product image.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.102 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the cards
    cards = soup.find_all("div", class_="ProductCard_root__mO63j")
    if not cards:
        print("No product cards found.")
        return []

    # Expected - newest cards are first
    cards = cards[:top_n]
    results = []

    for idx, card in enumerate(cards, start=1):
        card_data = {}

        # -- Product Image --
        image_tag = card.find("img")
        if image_tag and image_tag.has_attr("src"):
            image_url = image_tag["src"]
            card_data["image_url"] = image_url

            # Let's do card_image_# so they overwrite with new images
            image_filename = f"card_image_{idx}.jpg"
            download_image(image_url, image_filename)
            card_data["image_file"] = image_filename
        else:
            card_data["image_url"] = None
            card_data["image_file"] = None

        # -- Title --
        title_tag = card.find(attrs={"data-testid": "ProductCard-component-titleText"})
        card_data["title"] = title_tag.get_text(strip=True) if title_tag else None

        # -- Variant --
        variant_tag = card.find(attrs={"data-testid": "ProductCard-component-variantText"})
        card_data["variant"] = variant_tag.get_text(strip=True) if variant_tag else None

        # -- Distance --
        distance_tag = card.find(attrs={"data-testid": "ProductCard-component-distanceText"})
        card_data["distance"] = distance_tag.get_text(strip=True) if distance_tag else None

        # -- Transmission --
        transmission_tag = card.find(attrs={"data-testid": "ProductCard-component-transmissionText"})
        card_data["transmission"] = transmission_tag.get_text(strip=True) if transmission_tag else None

        # -- Price --
        price_tag = card.find(attrs={"data-testid": "ProductCard-component-priceText"})
        card_data["price"] = price_tag.get_text(strip=True) if price_tag else None

        # -- Repayment Info --
        repayment_tag = card.find(attrs={"data-testid": "ProductCard-component-repaymentText"})
        card_data["repayment_info"] = repayment_tag.get_text(strip=True) if repayment_tag else None

        results.append(card_data)

    return results

if __name__ == "__main__":
    url = "https://carma.com.au/"
    top_n = 3

    scraped_cards = scrape_carma_cards(url, top_n=top_n)
    if scraped_cards:
        print("Scraped Data:")
        for card in scraped_cards:
            print(card)
        
        # Save the JSON file
        output_file = "carma_scraped_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(scraped_cards, f, indent=4, ensure_ascii=False)
        print(f"Scraped data saved to {output_file}")
    else:
        print("No data was scraped.")
