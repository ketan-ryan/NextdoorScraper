import bs4
import time

# Create list of items we might be interested in
matches = ['exercise', 'equipment', 'dumbbell', 'wood']


def load_terms(terms=matches):
    global matches
    if terms != ['']:
        matches = terms


# Finds any postings that match what we want
def scrape(driver):
    # Get the html of the 'Finds' page
    html = driver.page_source
    time.sleep(2)

    soup = bs4.BeautifulSoup(html, 'lxml')
    links = []
    titles = []

    # For each card on the page, get the plaintext title as well as the link, and add them to the list
    for link in soup.findAll('a', attrs={'class': 'fsf-item-detail-link classified-item-card-container'}):
        title = (link.find('div').find('div', attrs={'class': 'classified-item-card'})
            .find('div', attrs={'class': 'classified-item-card-content'})
            .find('span', attrs={'class': 'classified-item-card-title css-1m53h5'}).contents[0])
        if any(x in str(title).lower() for x in matches):
            titles.append(title)
            links.append(link.get('href'))

    return links, titles


# Scrolls down the page. Default scroll height: 5
def scroll(driver, scroll_height=5):
    # Scroll a bit to load more items
    last_height = driver.execute_script('return document.body.scrollHeight')
    for i in range(scroll_height):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)  # Allow the page to load
        new_height = driver.execute_script('return document.body.scrollHeight')

        if new_height == last_height:
            break
        last_height = new_height
