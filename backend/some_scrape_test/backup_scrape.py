import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  
from database.mongodb_service import get_active_tracked_tickets
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
import time
import logging
import random
import os

# Set up logging to handle multi-threaded output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.propagate = False

def get_proxy():
    proxies = ["213.204.19.205:50100", "213.204.18.242:50100", "213.204.21.29:50100", "80.71.229.55:50100", "80.71.228.95:50100"] #proxiseller.com  FUNZIONANTI
    return random.choice(proxies)  

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; SM-A715F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Mozilla/5.0 (Linux; Android 9; SM-J730G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    ]
    return random.choice(user_agents)

def simulate_user_interaction(driver):
    actions = ActionChains(driver)
    actions.move_by_offset(5, 5).perform()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 3))
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(random.uniform(1, 3))

def get_chrome_main_version():
    chrome_path = uc.find_chrome_executable()
    bare_version = os.popen(f"{chrome_path} --version").read().strip()
    main_version = bare_version.split()[1].split('.')[0]
    return int(main_version)  

def find_ticket(searchQuery, queryTickets): 
    display = None
    driver = None 

    try:
        display = Display(visible=0, size=(1280, 800))
        display.start()
        version_main = get_chrome_main_version()
        switchProxies = True 
        checkIp = False
        profile_path = os.path.expanduser("/home/ubuntu/ticket-scraper/backend/chrome-profile")
     
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument(f'--user-data-dir={profile_path}') 
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x800')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--ignore-certificate-errors') 
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_argument(f'user-agent={get_random_user_agent()}')

        logger.info(f'Elaborating query: {searchQuery}')

        if switchProxies:
            proxy = get_proxy()
            logger.info(f'Using proxy: {proxy}')
            chrome_options.add_argument(f'--proxy-server={proxy}')
        
        driver = uc.Chrome(version_main=version_main, options=chrome_options, timeout=60)

        simulate_user_interaction(driver) 

        if checkIp:
            logger.info('Checking ip........')
            driver.get("https://whatismyipaddress.com/it/il-mio-ip")
            time.sleep(random.uniform(5, 10))
            event_html = driver.page_source
            event_soup = BeautifulSoup(event_html, 'html.parser')
            address_spans = event_soup.find_all('span', class_='address')
            logger.info(address_spans)

            return

        event_search_url = "https://www.fansale.it/events.htm?searchText=" + searchQuery
        driver.get(event_search_url)
        logger.info('Navigating event search page: ' + event_search_url)
        
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'SerpPage-SerpResultList-AllEntries')))

        event_html = driver.page_source
        event_soup = BeautifulSoup(event_html, 'html.parser')

        first_event = event_soup.find(class_='ListEntry-EVENT_SERIES')

        if first_event is None:
            logger.info('0 events found')
            return

        if first_event and 'href' in first_event.attrs:
            tickets_path = first_event['href']

            time.sleep(random.uniform(5, 10))
            tickets_url = "https://www.fansale.it" + tickets_path
            driver.get(tickets_url)
            logger.info('Navigating tickets page: ' + tickets_path)
            
            simulate_user_interaction(driver)

            time.sleep(random.uniform(5, 10))
            
            tickets_html = driver.page_source
            tickets_soup = BeautifulSoup(tickets_html, 'html.parser')

            tickets_container = tickets_soup.find(id='tabNormalFansaleEvents_panel')

            datestring_tracked = list(set([ticket['eventIsoDatetime'].split('T')[0] for ticket in queryTickets]))

            if tickets_container:
                a_tags = tickets_container.find_all('a')

                for a_tag in a_tags:
                    a_tags_ref = a_tag.get('href')
                    datestring = a_tag.get('data-tracking-eventdate')
                    if datestring in datestring_tracked:

                        date_tracked_ticket = [ticket for ticket in queryTickets if ticket['eventIsoDatetime'].split("T")[0] == datestring]

                        final_ticket_url = "https://www.fansale.it" + a_tags_ref
                        driver.get(final_ticket_url)
                        logger.info('Navigating finale ticket page: ' + final_ticket_url)
                        
                        simulate_user_interaction(driver)
                        time.sleep(random.uniform(5, 10))

                        final_ticket_html = driver.page_source
                        final_ticket_soup = BeautifulSoup(final_ticket_html, 'html.parser')
                        tab_container = final_ticket_soup.find('div', class_='EventEntryList')
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
