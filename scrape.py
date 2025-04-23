import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# SerpApi Access Key 
API_KEY = 'e7d0969dd7c1aee7a4c65c36ff2e2b9ce5e5c7cc5f3d2d01555834717086ea97'

# Function to get images from Google Images using SerpApi
def get_images_from_serpapi(query, num_images=5):
    search_url = "https://serpapi.com/search"
    params = {
        'q': query,
        'tbm': 'isch',  # This specifies image search
        'api_key': API_KEY,
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Extract image URLs from the response
        image_urls = []
        for image in data.get('images_results', [])[:num_images]:
            image_urls.append(image['original'])

        return image_urls
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching images: {e}")
        return []

# Streamlit UI
def main():
    st.title("Scrape Images from Google Search")

    # User input for image search
    prompt = st.text_input("Enter a prompt to search for images", "")

    # Display images when the user clicks the "Search" button
    if st.button("Search") and prompt:
        st.write(f"Fetching images for: {prompt}...")

        # Get images from Google via SerpApi
        image_urls = get_images_from_serpapi(prompt)

        # If images are found, display them
        if image_urls:
            st.write(f"Found {len(image_urls)} image(s).")
            for url in image_urls:
                try:
                    img_response = requests.get(url)
                    img = Image.open(BytesIO(img_response.content))
                    st.image(img, caption="Scraped Image", use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying image: {e}")
        else:
            st.warning("No images found. Please try another prompt.")

    elif not prompt:
        st.info("Enter a prompt and click 'Search'.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
