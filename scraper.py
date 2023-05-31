"""
Python Bot for SEO Description Generation

This script is a Python bot that generates SEO descriptions for products. It uses various libraries and APIs to scrape product information, generate descriptions using OpenAI's text generation model, and retrieve images from Google search.

Usage:
1. The bot install and updates automatically required libraries, however ensure that are installed correctly.
2. Provide a path to a CSV file containing product information. Should contain SKU and Name.
3. The bot will scrape each product's information, generate an SEO description, and retrieve an image.
4. The output will be written to an output.csv file, including the SKU, name, published status, description, short description, and image URL for each product.

Note: Please replace the placeholders for the OpenAI and SerpApi API keys with your own keys before running the bot.

GitHub Repository: <link to your GitHub repository>

Author: <Your Name>
Date: <Date>
"""

### THIS SECTION SEARCHES FOR LIBRARIES AND UPDATES

import csv
import importlib.util
import subprocess
import sys
import pkg_resources

required_libraries = ['requests', 'openai', 'bs4']

missing_libraries = []
outdated_libraries = []

for lib in required_libraries:
    spec = importlib.util.find_spec(lib)
    if spec is None:
        missing_libraries.append(lib)
    else:
        installed_version = pkg_resources.get_distribution(lib).version
        latest_version = subprocess.check_output([sys.executable, '-m', 'pip', 'show', lib]).decode("utf-8")
        latest_version = [line for line in latest_version.split("\n") if line.startswith("Version: ")][0].split(": ")[1]
        if installed_version != latest_version:
            outdated_libraries.append(lib)

if missing_libraries:
    print("The following libraries are missing:")
    for lib in missing_libraries:
        print(lib)
    print("Installing missing libraries...")

    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_libraries])
        print("Libraries installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install the missing libraries. Please install them manually and try again.")
        sys.exit(1)

if outdated_libraries:
    print("The following libraries have updates available:")
    for lib in outdated_libraries:
        print(lib)
    print("Updating libraries...")

    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', *outdated_libraries])
        print("Libraries updated successfully.")
    except subprocess.CalledProcessError:
        print("Failed to update the libraries. Please update them manually and try again.")
        sys.exit(1)



### THE ACTUAL CODE IS DOWN BELOW

import requests
import openai
from bs4 import BeautifulSoup
from urllib.parse import quote
from serpapi import GoogleSearch
import json

# Load the configuration file
with open("config.json") as f:
    config = json.load(f)

# Use the API keys from the configuration file
openai.api_key = config['openai_api_key']
SERP_API_KEY = config['serpapi_api_key']

def get_descriptions(search_term):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'https://duckduckgo.com/search?q={quote(search_term)}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all text blocks longer than 5 words and shorter than 450 words
    texts = soup.get_text().split()
    valid_texts = [' '.join(texts[i:i+5]) for i in range(0, len(texts), 5) if len(' '.join(texts[i:i+5])) < 450]

    return valid_texts

def generate_description(product_name, texts):
    # Prompt
    prompt = f"Create a detailed SEO description in Italian for the product {product_name} based on the following information: {texts}. Do not use commas (,). Do not nominate duckduckgo or javascript, just provide me the product description"

    attempts = 0
    while attempts < 3:
        try:
            # Generate a response
            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=600,
                n=1,
                stop=None,
                temperature=0.2,
            )

            return completion.choices[0].text.strip()

        except Exception as e:
            print(f"Error occurred while generating description for {product_name}. Attempt {attempts+1} failed. Error: {e}")
            attempts += 1

    print(f"Failed to generate description for {product_name} after 3 attempts. Skipping.")
    return None


def google_image_scraper(query, start_index=1, num_results=1):
    params = {
        "engine": "google",
        "q": query,
        "tbm": "isch",
        "start": start_index,
        "num": num_results,
        "api_key": SERP_API_KEY,  
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    #image_urls = []

    try:
        if "images_results" in results:
            image_urls = [img["original"] for img in results["images_results"]]
    except KeyError as e:
        print(f"Error occurred while scraping image for {query}. Skipping. Error: {e}")
    
    return image_urls[:num_results]


def write_to_csv(output_data):
    with open('output.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SKU", "Name", "Published", "Description", "Short description", "Price", "Image"])
        for row in output_data:
            product_code, name, description, price, image = row
            if description is not None:
                writer.writerow([product_code, name, 1, description, description[:100], price, image])  # Include image as part of the list
            else:
                print(f"Failed to write product {name} to CSV because its description is None.")
                writer.writerow([product_code, name, 1, 'Insert Description', 'Insert Short Description', price, image])



def main():
    output_data = []
    csv_file_path = config['csv_file_path']  #CSV file path from the configuration file
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Scraping
            product_code, name, price = row[:3]
            print(f"Scraping for {name}...")
            texts = get_descriptions(name)
            print("Scraping completed for the product.\n")

            # Generating SEO description
            print(f"Generating description for {name}...")
            description = generate_description(name, texts)
            if description is not None:
                print("Generation completed for the product.\n")
            
            # Scraping Image
            image_url = []
            if config['image_scraping_enabled']:
                print(f"Scraping Image for for {name}...")
                image_url = google_image_scraper(name, start_index=1, num_results=1)
                print("Scraping completed for the product\n")

            output_data.append([product_code, name, description, price, image_url])
            write_to_csv(output_data)
            print("Succesfully added in the csv")
    
    print("\nScraping Finished!")

if __name__ == "__main__":
    main()