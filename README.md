# 🚀 Woocommerce Product SEO Description and Image Scraper Bot 🚀

This Python bot automatically generates SEO descriptions for products and scrapes related images using OpenAI's text generation model and the SerpApi image search. It reads product information from a CSV file in the Woocommerce format and writes the generated descriptions and image URLs back to another CSV file.

## 👨‍💻 How to Use 👨‍💻

1. **Install the required libraries**: The bot checks for missing or outdated libraries and installs/updates them. Ensure that pip, Python's package installer, is set up on your system.

2. **Modify the `config.json` file**: The `config.json` file in the same directory as the Python script holds the configuration. Here's what each key means:

   - `openai_api_key`: Your OpenAI API key. The bot uses this key to generate product descriptions.
   - `serpapi_api_key`: Your SerpApi API key. The bot uses this key to scrape product images.
   - `csv_file_path`: The path to the CSV file that contains your product information. The bot reads this file to get the list of products.
   - `num_images`: The number of images to search for each product.

3. **Run the bot**: You can run the bot using the command `python <filename>.py`. The bot will read the product information from the CSV file specified in the `config.json` file, generate an SEO description for each product, scrape a number of images specified in the `config.json` file, and write the results back to an `output.csv` file in the same directory as the Python script.

4. **Review the results**: The `output.csv` file will include the SKU, name, published status, generated description, short description, and image URL for each product.

Please replace `<your_openai_api_key_here>`, `<your_serpapi_api_key_here>`, `<path_to_your_csv_file_here>`, and `<number_of_images_per_product>` with your actual OpenAI API key, SerpApi API key, CSV file path, and number of images per product, respectively.

📖 Note 📖
The SEO description generation and image scraping are automated processes and might not always produce perfect results. Please review the output CSV file and make any necessary adjustments manually.

Happy scraping! 🎉