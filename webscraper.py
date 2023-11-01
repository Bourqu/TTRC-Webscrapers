from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Create or open the CSV file for writing data
with open('output.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    csv_writer = csv.writer(csvfile)

    # Write the header row
    csv_writer.writerow(['Page Title', 'Owner', 'File Formats', 'Description', 'Date Last Updated', 'License', 'Update Frequency', 'Access'])

    # Read the list of URLs from the text file
    with open('url_list.txt', 'r') as url_file:
        url_list = url_file.read().splitlines()

    count= 1
    # Iterate through the list of URLs
    for url in url_list:
        try:
            # Navigate to the URL
            driver.get(url)

            # Wait for some time to let the page load
            time.sleep(1)

            # Get the page title
            page_title = driver.title

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Try-except blocks for each item extraction
            try:
                owner = soup.find('dd', attrs={'data-field': "owner_division"}).text
            except AttributeError:
                owner = ''

            try:
                formats = soup.find('div', class_='format').text
            except AttributeError:
                formats = ''

            try:
                description = soup.find('div', attrs={'data-field': "notes"}).find('p').text
            except AttributeError:
                description = ''

            try:
                last_access = soup.find('dd', attrs={'data-field': "last_refreshed"}).text
            except AttributeError:
                last_access = ''

            try:
                license = soup.find_all('a', class_="inline-link")[-1].text
            except (AttributeError, IndexError):
                license = ''

            try:
                refresh_rate = soup.find('dd', attrs={'data-field': "refresh_rate"}).text
            except AttributeError:
                refresh_rate = ''

            # Find the iframe element
            table_url = soup.find('iframe')

            # Extract the source URL of the iframe
            iframe_src = table_url['src']

            # Navigate to the iframe URL
            driver.get(iframe_src)

            # Get the HTML content of the iframe as a string
            iframe_html = driver.page_source

            # Now you can parse the iframe content using BeautifulSoup if needed
            iframe_soup = BeautifulSoup(iframe_html, 'html.parser')

            # Try to extract the 'access' variable, set to an empty string if it doesn't work
            try:
                access = iframe_soup.find_all("span", class_="text-muted")[-1].text
            except (AttributeError,IndexError):
                access = ''

            # Write the data to the CSV file
            csv_writer.writerow([page_title, owner, formats, description, last_access, license, refresh_rate, access])

        except Exception as e:
            print(f"An error occurred while processing URL {url}: {str(e)}")

        
        print(page_title,count,"of 205")
        count+=1
# Close the WebDriver
driver.quit()
