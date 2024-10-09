import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  
#from database.mongodb_service import get_active_tracked_tickets
from update_and_notify import update_and_notify
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
import time
import logging
import random
import os


logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/home/ubuntu/ticket-scraper/backend/logs/scrape.log"), 
        logging.StreamHandler()  
    ]
)


logger = logging.getLogger(__name__)

def get_proxy():
    proxies = [
    "213.204.18.58:50100",
    "213.204.18.49:50100",
    "213.204.18.46:50100",
    "213.204.18.43:50100",
    "213.204.18.38:50100",
    "213.204.18.36:50100",
    "213.204.18.33:50100",
    "80.71.228.162:50100",
    "213.204.19.189:50100",
    "213.204.18.76:50100",
    "213.204.21.17:50100",
    "213.204.21.233:50100",
    "213.204.21.146:50100",
    "213.204.19.188:50100",
    "213.204.18.186:50100",
    "213.204.19.177:50100",
    "213.204.18.82:50100",
    "213.204.18.81:50100",
    "213.204.18.80:50100",
    "213.204.19.184:50100",
    "213.204.19.197:50100",
    "213.204.18.68:50100",
    "213.204.19.34:50100",
    "213.204.18.121:50100",
    "213.204.19.70:50100",
    "213.204.19.88:50100",
    "213.204.18.108:50100",
    "213.204.18.109:50100",
    "213.204.19.222:50100",
    "213.204.21.6:50100",
    "213.204.19.91:50100",
    "213.204.19.99:50100",
    "213.204.18.191:50100",
    "213.204.18.199:50100",
    "213.204.21.103:50100",
    "213.204.21.104:50100",
    "213.204.21.107:50100",
    "213.204.18.48:50100",
    "213.204.18.23:50100",
    "213.204.18.22:50100",
    "213.204.21.143:50100",
    "213.204.21.149:50100",
    "213.204.18.8:50100",
    "213.204.21.155:50100"] #proxiseller.com  FUNZIONANTI
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

def find_ticket(searchQuery, queryTickets, nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent): 
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
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("""Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});""")
        driver.execute_script("Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4});")
        driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});")
        driver.execute_script("""Object.defineProperty(HTMLCanvasElement.prototype, 'toDataURL', {
                value: function() {
                    return "data:image/png;base64,spoofedcanvasdata";
                }
            });""")
        

        '''
        navigator_properties = driver.execute_script("""
            // Return an object containing various navigator properties
            return {
                webdriver: navigator.webdriver,            
                userAgent: navigator.userAgent,         
                platform: navigator.platform,           
                language: navigator.language,      
                hardwareConcurrency: navigator.hardwareConcurrency, 
                deviceMemory: navigator.deviceMemory  
            };
        """)
        logger.info(f"Navigator properties: {navigator_properties}")
        '''

        simulate_user_interaction(driver) 

        if checkIp:
            logger.info('Checking ip........')
            driver.get("https://whatismyipaddress.com/it/il-mio-ip")
            event_html = driver.page_source
            event_soup = BeautifulSoup(event_html, 'html.parser')
            address_spans = event_soup.find_all('span', class_='address')
            logger.info(address_spans)

        event_search_url = "https://www.fansale.it/events.htm?searchText=" + searchQuery
        driver.get(event_search_url) #low antiscraping measures
        logger.info('Navigating event search page: ' + event_search_url)
        
        #WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'SerpPage-SerpResultList-AllEntries')))
        time.sleep(random.uniform(2, 5))


        event_html = driver.page_source
        event_soup = BeautifulSoup(event_html, 'html.parser')
        logger.info(event_soup)
        

        first_event = event_soup.find(class_='ListEntry-EVENT_SERIES')


        if first_event is None:
            logger.info('0 events found')
            return nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent

        if first_event and 'href' in first_event.attrs:
            nrFoundEventsChecked += 1
            tickets_path = first_event['href']

            time.sleep(random.uniform(1, 3))
            tickets_url = "https://www.fansale.it" + tickets_path
            driver.get(tickets_url) #high antiscraping measures
            logger.info('Navigating tickets page: ' + tickets_path)
            
            simulate_user_interaction(driver)
            time.sleep(random.uniform(1, 3))
            
            tickets_html = driver.page_source
            tickets_soup = BeautifulSoup(tickets_html, 'html.parser')

            tickets_container = tickets_soup.find(id='tabNormalFansaleEvents_panel')

            if tickets_container:
                logger.info('✅ Found tickets container in tickets page')
            else:
                logger.info('❌ Ticket container not found in ticket page, probably detected by antiscraping.')


            datestring_tracked = list(set([ticket['eventIsoDatetime'].split('T')[0] for ticket in queryTickets]))

            if tickets_container:
                a_tags = tickets_container.find_all('a')

                for a_tag in a_tags:
                    a_tags_ref = a_tag.get('href')
                    datestring = a_tag.get('data-tracking-eventdate')
                    if datestring in datestring_tracked:
                        nrFinalTicketPageChecked += 1

                        date_tracked_ticket = [ticket for ticket in queryTickets if ticket['eventIsoDatetime'].split("T")[0] == datestring]

                        final_ticket_url = "https://www.fansale.it" + a_tags_ref
                        driver.get(final_ticket_url) #high antiscraping measures
                        logger.info('Navigating final ticket page: ' + final_ticket_url)
                        
                        simulate_user_interaction(driver)
                        time.sleep(random.uniform(1, 3))

                        final_ticket_html = driver.page_source
                        final_ticket_soup = BeautifulSoup(final_ticket_html, 'html.parser')
                        tab_container = final_ticket_soup.find('div', class_='EventEntryList')

                        if tab_container:
                            logger.info('✅ Found Tab container in final ticket page')
                        else:
                            logger.info('❌ Tab container not found in final ticket page, probably detected by antiscraping.')
                        
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

                        notifSent += 1

                        update_and_notify(matching_users)


    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    finally:
        if driver:
            driver.quit()
        if display:
            display.stop()

    return nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent



lock_file_path = "/home/ubuntu/ticket-scraper/backend/scraper.lock"  

def acquire_lock():
    if os.path.exists(lock_file_path):
        logger.info("Lock file exists. Script is already running.")
        return False
    else:
        with open(lock_file_path, "w") as lock_file:
            lock_file.write(str(os.getpid()))  
        return True

def release_lock():
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)

def main():
    process_id = os.getpid()  
    start_time = time.time() 
    nrSearchQueries = 0 
    nrFoundEventsChecked = 0 
    nrFinalTicketPageChecked = 0
    notifSent = 0

    if not acquire_lock():
        return
    
    try:
        logger.info("\n\n") 
        logger.info(f"🚀 Starting new process (ID: {process_id})")  

        tracked_tickets = get_active_tracked_tickets()
        searchQueryList = list(set([ticket['eventName'] for ticket in tracked_tickets]))

        logger.info(f'Search query list: {searchQueryList}')
        
        for searchQuery in searchQueryList:
            nrSearchQueries += 1
            queryTickets = [ticket for ticket in tracked_tickets if ticket['eventName'] == searchQuery]
            nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent = find_ticket(searchQuery, queryTickets, nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent)

    except Exception as e:
        logger.error(f"An error occurred in process {process_id}: {str(e)}")

    finally:
        end_time = time.time() 
        duration_seconds = end_time - start_time  
        duration_minutes = duration_seconds / 60
        logger.info(f"🏁 Process completed (ID: {process_id}) - Duration: {duration_minutes:.2f} min, Search pages scraped: {nrSearchQueries} and found {nrFoundEventsChecked} Available Events pages scraped, Final Ticket pages scraped: {nrFinalTicketPageChecked}, Notification sent: {notifSent}") 
        release_lock()

if __name__ == "__main__":
    main()