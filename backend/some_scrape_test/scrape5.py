import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from database.mongodb_service import get_active_tracked_tickets
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium.webdriver.common.action_chains import ActionChains 
import time
import logging
import random
import os


# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.FileHandler("/home/ubuntu/ticket-scraper/backend/logs/scrape.log"),  # Write logs to a file
        logging.StreamHandler()  # Also print logs to stdout (console)
    ]
)

# Example of using the logger
logger = logging.getLogger(__name__)

def get_proxy():
    proxies = ["213.204.19.205:50100", "213.204.18.242:50100", "213.204.21.29:50100", "80.71.229.55:50100", "80.71.228.95:50100"] #proxiseller.com  FUNZIONANTI
    return random.choice(proxies)  

def get_random_user_agent():
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.89 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6040.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6116.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6151.44 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6204.58 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6252.80 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6308.76 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6373.112 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6421.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6479.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6534.62 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6590.50 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6647.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6701.45 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6754.33 Safari/537.36']
    return random.choice(user_agents)


def get_chrome_main_version():
    chrome_path = uc.find_chrome_executable()
    bare_version = os.popen(f"{chrome_path} --version").read().strip()
    main_version = bare_version.split()[1].split('.')[0]
    return int(main_version)  

def simulate_user_interaction(driver):
    actions = ActionChains(driver)
    actions.move_by_offset(5, 5).perform()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 3))
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(random.uniform(1, 3))


def open_chrome_with_proxy(version_main, url, switchProxies, checkIp, simulateUser=False):

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x800')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--ignore-certificate-errors') 
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_argument(f'user-agent={get_random_user_agent()}')

    logger.info(f'Elaborating query: {searchQuery}')

    proxy = 'noproxy'
    if switchProxies:
        proxy = get_proxy()
        logger.info(f'Using proxy: {proxy}')
        chrome_options.add_argument(f'--proxy-server={proxy}')

    profile_path = os.path.expanduser(f"/home/ubuntu/ticket-scraper/backend/chrome-profile/{proxy}")
    chrome_options.add_argument(f'--user-data-dir={profile_path}') 

    if checkIp:
        logger.info('Checking ip........')
        driver.get("https://whatismyipaddress.com/it/il-mio-ip")
        event_html = driver.page_source
        event_soup = BeautifulSoup(event_html, 'html.parser')
        address_spans = event_soup.find_all('span', class_='address')
        logger.info(address_spans)

    driver = uc.Chrome(version_main=version_main, options=chrome_options, timeout=60)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("""Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});""")
    driver.execute_script("Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4});")
    driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});")

    '''
    navigator_properties = driver.execute_script("""
        // Return an object containing various navigator properties
        return {
            webdriver: navigator.webdriver,            // Check if WebDriver is present (indicates automation)
            userAgent: navigator.userAgent,            // Browser's user agent string
            platform: navigator.platform,              // The platform the browser is running on (e.g., Windows, Linux)
            language: navigator.language,              // Browser's language setting
            hardwareConcurrency: navigator.hardwareConcurrency,  // Number of logical processor cores
            deviceMemory: navigator.deviceMemory       // Approximate device memory in gigabytes
        };
    """)

    logger.info(f"Navigator properties: {navigator_properties}")
    '''


    driver.get(url)

    if simulateUser:
        simulate_user_interaction(driver) 
        time.sleep(random.uniform(3, 5))

    
    return driver


def find_ticket(searchQuery, queryTickets): 
    display = None
    driver = None 

    try:
        display = Display(visible=0, size=(1280, 800))
        display.start()
        version_main = get_chrome_main_version()
        switchProxies = True 
        checkIp = False

        event_search_url = "https://www.fansale.it/events.htm?searchText=" + searchQuery
        driver = open_chrome_with_proxy(version_main, event_search_url, switchProxies, checkIp)
        
        logger.info('Navigating event search page: ' + event_search_url)
        
        event_html = driver.page_source
        event_soup = BeautifulSoup(event_html, 'html.parser')

        first_event = event_soup.find(class_='ListEntry-EVENT_SERIES')
       
        if first_event is None:
            logger.info('Event not found')
            return
        else:
            logger.info('Event found')

        if first_event and 'href' in first_event.attrs:
            tickets_path = first_event['href']
            tickets_url = "https://www.fansale.it" + tickets_path

            driver.quit()
            driver = open_chrome_with_proxy(version_main, tickets_url, switchProxies, checkIp, True)

            logger.info('Navigating tickets page: ' + tickets_path)

            tickets_html = driver.page_source
            tickets_soup = BeautifulSoup(tickets_html, 'html.parser')

            tickets_container = tickets_soup.find(id='tabNormalFansaleEvents_panel')

            if tickets_container:
                logger.info('Found tickets container in tickets page')
            else:
                logger.info('Ticket container not found in ticket page, probably detected by antiscraping.')



            datestring_tracked = list(set([ticket['eventIsoDatetime'].split('T')[0] for ticket in queryTickets]))

            if tickets_container:
                a_tags = tickets_container.find_all('a')

                for a_tag in a_tags:
                    a_tags_ref = a_tag.get('href')
                    datestring = a_tag.get('data-tracking-eventdate')
                    if datestring in datestring_tracked:

                        date_tracked_ticket = [ticket for ticket in queryTickets if ticket['eventIsoDatetime'].split("T")[0] == datestring]

                        final_ticket_url = "https://www.fansale.it" + a_tags_ref

                        driver.quit()
                        logger.info('Navigating finale ticket page: ' + final_ticket_url)
                        driver = open_chrome_with_proxy(version_main, final_ticket_url, switchProxies, checkIp, True)

                        final_ticket_html = driver.page_source
                        final_ticket_soup = BeautifulSoup(final_ticket_html, 'html.parser')
                        tab_container = final_ticket_soup.find('div', class_='EventEntryList')

                        if tab_container:
                            logger.info('Found Tab container in final ticket page')
                        else:
                            logger.info('Tab container not found in final ticket page, probably detected by antiscraping.')
                        
                        quantities_span = [span.get_text(strip=True) for span in tab_container.find_all('span', class_='NumberOfTicketsInOffer')]
                        quantities_options = [option.get_text(strip=True) for option in tab_container.find_all('option')]
                        quantities = quantities_span + quantities_options
                        quantities = [int(q) for q in quantities]
                        unique_quantities = list(set(quantities))
                        unique_quantities.sort(reverse=True)
                        bigger_qty = unique_quantities[0]

                        matching_users = [
                            {**user, 'final_ticket_url': final_ticket_url} 
                            for user in date_tracked_ticket 
                            if user['nrTickets'] <= bigger_qty
                        ]

                        logger.info(matching_users)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    finally:
        if driver:
            driver.quit()
        if display:
            display.stop()



if __name__ == "__main__":

    tracked_tickets = get_active_tracked_tickets()
    searchQueryList = list(set([ticket['eventName'] for ticket in tracked_tickets]))

    logger.info(f'Search query list: {searchQueryList}')
    
    for searchQuery in searchQueryList:
        queryTickets = [ticket for ticket in tracked_tickets if ticket['eventName'] == searchQuery]
        find_ticket(searchQuery, queryTickets)


