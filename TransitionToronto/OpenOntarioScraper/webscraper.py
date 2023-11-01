from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"

# Configure Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument(f"--user-agent={user_agent}")
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

    count=1

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

            # Try-except blocks for each item extraction******************
            try:
                owner = soup.find('h3', attrs={'itemprop': "sourceOrganization"}).text.replace(","," ").strip()
            except AttributeError:
                owner = ''

            try:
                formats = soup.find('span',attrs={'property':"dc:format"}).text
            except AttributeError:
                formats = ''

            try:
                description = soup.find('div', attrs={'itemprop': "description"}).find('p').text.replace(","," ").strip()
            except AttributeError:
                description = ''

            try:
                last_access = soup.find('p', class_="description details").text.split(":")[1].strip()
            except (AttributeError,IndexError):
                last_access = ''

            try:
                license = soup.find('a', attrs={'itemprop':'license'} ).text
            except (AttributeError, IndexError):
                license = ''

            try:
                refresh_rate = soup.find_all('td', class_="dataset-details")[-1].text.strip()
            except (AttributeError,IndexError):
                refresh_rate = ''

            
            try:
                geo_access = soup.find('td',attrs={'itemprop':'spatialCoverage'} ).text.strip()
            except (AttributeError, IndexError):
                geo_access = "" 

        # Write the data to the CSV file
            csv_writer.writerow([page_title, owner, formats, description, last_access, license, refresh_rate, "", geo_access])

        except Exception as e:
            print(f"An error occurred while processing URL {url}: {str(e)}")

        print(page_title,count,"of 404")
        count+=1
# Close the WebDriver
driver.quit()
