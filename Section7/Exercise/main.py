import streamlit as st
import pandas as pd
import requests


# Function to make a GET request
@st.cache_data(show_spinner="Searching...")
def make_get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        response = response.json()  
        if len(response['results']) == 0:
            return False
        else:
            return response
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while making the GET request: {e}")
        return False


@st.cache_data(show_spinner="Searching...")
def search_gutenberg(author, title):
    # Define your base url
    params = author.lower() + " " + title.lower()
    params = params.strip()
    params = params.replace(" ", "%20")
    url = f"https://gutendex.com/books?search={params}"
    # Replace whitespace with %20 as per the documentation
    # For the search parameters

    # Make a url from the search parameters

    # Make the final search url (combine base with params url)

    try:
        response = make_get_request(url)
        
       
        if 'results' not in response:
            return False
        else:
            return response

        # Get the JSON response

        # If your JSON has no results, return False
        # Else, return the JSON reponse
    except:
        return False

# Function to format the JSON response as a DataFrame


@st.cache_data
def format_json_res(json_res):
    cols = ['Id', 'Author', 'Title', 'Language', 'Link']

    rows = []

    try:
        for i in range(len(json_res['results'])):
            book = json_res['results'][i]
            book_id = book['id']
            book_author = book['authors'][0]['name'] if len(book['authors']) > 0 else "Unknown"
            book_title = book['title']
            book_language = book['languages'][0] if len(book['languages']) > 0 else "Unknown"
            book_link = f"https://www.gutenberg.org/ebooks/{book_id}"

            rows.append([book_id, book_author, book_title, book_language, book_link])

        df = pd.DataFrame(rows, columns=cols)

        return df
    except:
        st.error("Error while parsing data")


if __name__ == "__main__":
    st.title("📚 Search Project Gutenberg")
    with st.form("search-form"):
        col1, col2 = st.columns(2)

        with col1:
            author = st.text_input("Author")
        with col2:
            title = st.text_input("Title")

        search = st.form_submit_button("Search", type='primary')
        if search:
            if author == "" and title == "":
                st.error("Please enter at least one search parameter")
            else:
                json_res = search_gutenberg(author, title)
                if json_res:
                    df = format_json_res(json_res)
                    st.dataframe(df)
                else:
                    st.error("No results found")