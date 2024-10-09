import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  
from update_and_notify import update_and_notify
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from sqs_utils import get_message_10batch_and_delete
from logging.handlers import RotatingFileHandler
import requests
import json
import time
import logging
import random
import os 
from datetime import datetime
import sys  
from contextlib import contextmanager
import signal
import subprocess
import tempfile
import psutil
import shutil
import traceback
import gc

# Define the log file path
log_file_path = "/home/ubuntu/ticket-scraper/backend/logs/scrape.log"
update_parameter_url = 'http://18.102.166.102/update_parameter'

# Set up the logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        RotatingFileHandler(log_file_path, maxBytes=1024*1024, backupCount=3),  # 1MB file size, keep 5 backups
        logging.StreamHandler()  # Also print logs to stdout (console)
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
    "213.204.21.155:50100"] #proxiseller.com account Luigi   

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


def restart_chromium():
    # Terminate all Chromium processes
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'chromium' in proc.info['name'].lower():
            try:
                proc.kill()
                logger.info(f"Killed process: {proc.pid}")
            except Exception as e:
                logger.error(f"Error killing process {proc.pid}: {e}")

    # Remove temporary directories if any
    temp_dirs = ['/tmp/chromium', '/tmp/ChromiumCache']  # Add any directories used by Chromium
    for temp_dir in temp_dirs:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info(f"Removed temporary directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Error removing temporary directory {temp_dir}: {e}")

def get_chrome_main_version(chrome_path, retries=3, delay=2):
    logger.info(f"Using Chrome executable at: {chrome_path}")
    if not chrome_path or not os.path.exists(chrome_path):
        logger.error(f"Chrome executable not found at {chrome_path}.")
        raise RuntimeError("Chrome executable not found.")

    for attempt in range(retries):
        try:
            bare_version = subprocess.check_output(
                [chrome_path, '--version'],
                stderr=subprocess.STDOUT,
                text=True
            ).strip()
            # Adjust parsing based on the browser
            if 'Chromium' in bare_version:
                version_str = bare_version.replace('Chromium', '').strip()
            elif 'Google Chrome' in bare_version:
                version_str = bare_version.replace('Google Chrome', '').strip()
            else:
                version_str = bare_version
            main_version = version_str.split('.')[0]
            logger.info(f"Detected Chrome main version: {main_version}")
            return int(main_version)
        except subprocess.CalledProcessError as e:
            logger.error(f"Attempt {attempt + 1}: Error executing '{chrome_path} --version': {e.output}")
            time.sleep(delay)
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}: Error parsing Chrome version from {chrome_path}: {e}")
            time.sleep(delay)
    raise RuntimeError(f"Failed to get Chrome version after {retries} attempts")

@contextmanager
def managed_display():
    display = Display(visible=0, size=(1280, 800))
    display.start()
    try:
        yield display
    finally:
        display.stop()

@contextmanager
def managed_driver(version_main, chrome_options, chrome_path):
    if not os.path.exists(chrome_path):
        logger.error(f"Chrome executable not found at {chrome_path}.")
        raise RuntimeError("Chrome executable not found.")

    driver = uc.Chrome(
        version_main=version_main,
        options=chrome_options,
        browser_executable_path=chrome_path,  # Dynamic path to Chromium
        timeout=60
    )
    try:
        yield driver
    finally:
        driver.quit()


def log_resource_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)  # in MB
    cpu = psutil.cpu_percent(interval=None)  # Non-blocking
    logger.info(f"CPU usage: {cpu:.2f}% | Memory usage: {mem:.2f} MB")

    
def find_ticket(searchQuery, queryTickets, nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent): 
    try:
        with tempfile.TemporaryDirectory() as profile_path:
            with managed_display():
                switchProxies = True 
                chrome_path = '/bin/chromium-browser'  # instead that return 2 different randm symlink, taht is the same result anyway uc.find_chrome_executable()
                version_main = get_chrome_main_version(chrome_path, retries=3, delay=2)
                checkIp = False

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

                with managed_driver(version_main, chrome_options, chrome_path) as driver:
                    # Navigator spoofing scripts
                    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    driver.execute_script("""Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});""")
                    driver.execute_script("Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4});")
                    driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});")
                    driver.execute_script("""Object.defineProperty(HTMLCanvasElement.prototype, 'toDataURL', {
                            value: function() {
                                return "data:image/png;base64,spoofedcanvasdata";
                            }
                        });""")

                    simulate_user_interaction(driver)

                    if checkIp:
                        logger.info('Checking ip........')
                        driver.get("https://whatismyipaddress.com/it/il-mio-ip")
                        event_html = driver.page_source
                        event_soup = BeautifulSoup(event_html, 'html.parser')
                        address_spans = event_soup.find_all('span', class_='address')
                        logger.info(address_spans)

                    event_search_url = "https://www.fansale.it/events.htm?searchText=" + searchQuery
                    driver.get(event_search_url)  # low antiscraping measures
                    logger.info('Navigating event search page: ' + event_search_url)
                    
                    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'SerpPage-SerpResultList-AllEntries')))

                    event_html = driver.page_source
                    event_soup = BeautifulSoup(event_html, 'html.parser')
                    
                    first_event = event_soup.find(class_='ListEntry-EVENT_SERIES')

                    if first_event is None:
                        logger.info('0 events found')
                        return nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent

                    if first_event and 'href' in first_event.attrs:
                        nrFoundEventsChecked += 1
                        tickets_path = first_event['href']

                        time.sleep(random.uniform(1, 3))
                        tickets_url = "https://www.fansale.it" + tickets_path
                        driver.get(tickets_url)  # high antiscraping measures
                        logger.info('Navigating tickets page: ' + tickets_path)
                        
                        simulate_user_interaction(driver)
                        time.sleep(random.uniform(1, 3))
                        
                        tickets_html = driver.page_source
                        tickets_soup = BeautifulSoup(tickets_html, 'html.parser')

                        tickets_container = tickets_soup.find(id='tabNormalFansaleEvents_panel')

                        if tickets_container:
                            logger.info('✅ Found tickets container in tickets page')
                        else:
                            current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            payload = {'parameter_name': 'antiscraper_detected', 'parameter_value': f'ticket page - {current_datetime}'}
                            headers = {'Content-Type': 'application/json'}
                            try:
                                response = requests.post(update_parameter_url, json=payload, headers=headers)
                                if response.status_code != 200:
                                    logger.error(f"Failed to update antiscraper_detected parameter on master server")
                            except Exception as e:
                                logger.error(f"Failed to send antiscraper_detected update: {e}")

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
                                    driver.get(final_ticket_url)  # high antiscraping measures
                                    logger.info('Navigating final ticket page: ' + final_ticket_url)
                                    
                                    simulate_user_interaction(driver)
                                    time.sleep(random.uniform(1, 3))

                                    final_ticket_html = driver.page_source
                                    final_ticket_soup = BeautifulSoup(final_ticket_html, 'html.parser')
                                    tab_container = final_ticket_soup.find('div', class_='EventEntryList')

                                    if tab_container:
                                        logger.info('✅ Found Tab container in final ticket page')
                                    else:
                                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                        payload = {'parameter_name': 'antiscraper_detected', 'parameter_value': f'final ticket page - {current_datetime}'}
                                        headers = {'Content-Type': 'application/json'}
                                        try:
                                            response = requests.post(update_parameter_url, json=payload, headers=headers)
                                            if response.status_code != 200:
                                                logger.error(f"Failed to update antiscraper_detected parameter on master server")
                                        except Exception as e:
                                            logger.error(f"Failed to send antiscraper_detected update: {e}")

                                        logger.info('❌ Tab container not found in final ticket page, probably detected by antiscraping.')
                                    
                                    # Extract quantities
                                    quantities_span = [span.get_text(strip=True) for span in tab_container.find_all('span', class_='NumberOfTicketsInOffer')]
                                    quantities_options = [option.get_text(strip=True) for option in tab_container.find_all('option')]
                                    quantities = quantities_span + quantities_options
                                    try:
                                        quantities = [int(q) for q in quantities]
                                    except ValueError as e:
                                        logger.error(f"Error converting quantities to integers: {e}")
                                        quantities = []
                                    unique_quantities = list(set(quantities))
                                    unique_quantities.sort(reverse=True)
                                    bigger_qty = unique_quantities[0] if unique_quantities else 0

                                    # Match users
                                    matching_users = [
                                        {**user, 'final_ticket_url': final_ticket_url} 
                                        for user in date_tracked_ticket 
                                        if user.get('nrTickets', 0) <= bigger_qty
                                    ]

                                    notifSent += 1

                                    update_and_notify(matching_users)

                                    # Cleanup large variables
                                    del final_ticket_html, final_ticket_soup, tab_container, quantities_span, quantities_options, quantities, unique_quantities, bigger_qty, matching_users
                                    gc.collect()

                        # Cleanup after processing tickets
                        del event_html, event_soup, first_event, tickets_container, tickets_html, tickets_soup, a_tags, a_tags_ref, datestring, datestring_tracked
                        gc.collect()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())

    return nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent

lock_file_path = "/home/ubuntu/ticket-scraper/backend/scraper.lock"  

def acquire_lock():
    if os.path.exists(lock_file_path):
        #logger.info("Lock file exists. Script is already running.")
        return False
    else:
        with open(lock_file_path, "w") as lock_file:
            lock_file.write(str(os.getpid()))
        return True

def release_lock():
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)

@contextmanager
def lock_script():
    if not acquire_lock():
        #logger.info("Another instance is running. Exiting.")
        sys.exit(0)
    try:
        yield
    finally:
        release_lock()
        logger.info("Lock released.")

def handle_signal(signum, frame):
    logger.info(f"Received signal {signum}. Releasing lock and exiting.")
    release_lock()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    with lock_script():
        process_id = os.getpid()
        start_time = time.time()
        nrSearchQueries = 0
        nrFoundEventsChecked = 0
        nrFinalTicketPageChecked = 0
        notifSent = 0

        try:
            logger.info("\n\n")
            logger.info(f"🚀 Starting new process (ID: {process_id})")

            try:
                messages = get_message_10batch_and_delete()

                if not isinstance(messages, list):
                    logger.error("Fetched messages are not in a list format.")
                    messages = []
            except Exception as e:
                logger.error(f"Error fetching messages: {e}")
                messages = []

            tracked_tickets = []
            for idx, message in enumerate(messages):
                try:
                    receipt_handle = message.get('ReceiptHandle')
                    body = message.get('Body')

                    if not receipt_handle or not body:
                        logger.error(f"Message at index {idx} missing 'ReceiptHandle' or 'Body': {message}")
                        continue

                    ticket_data = json.loads(body)
                    event_name = ticket_data.get('eventName')

                    if not event_name:
                        logger.error(f"Ticket data missing 'eventName': {ticket_data}")
                        continue

                    tracked_ticket = {'ReceiptHandle': receipt_handle, **ticket_data}
                    tracked_tickets.append(tracked_ticket)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decoding error for message at index {idx}: {e} - Body: {body}")
                except Exception as e:
                    logger.error(f"Unexpected error processing message at index {idx}: {e}")

            if not tracked_tickets:
                logger.warning("No valid tracked tickets found. Exiting.")
                return  # Exit the function

            searchQueryList = list(set([ticket['eventName'] for ticket in tracked_tickets]))
            logger.info(f'Search query list: {searchQueryList}')

            for searchQuery in searchQueryList:
                nrSearchQueries += 1
                queryTickets = [ticket for ticket in tracked_tickets if ticket.get('eventName') == searchQuery]
                nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent = find_ticket(
                    searchQuery, queryTickets, nrFoundEventsChecked, nrFinalTicketPageChecked, notifSent
                )

                # Remove processed tickets to free memory
                tracked_tickets = [ticket for ticket in tracked_tickets if ticket.get('eventName') != searchQuery]

                #garbage collection
                gc.collect()

        except Exception as e:
            logger.error(f"An error occurred in process {process_id}: {str(e)}")
            logger.error(traceback.format_exc())
            sys.exit(1)  # Exit with non-zero status code to indicate failure

        finally:
            end_time = time.time()
            duration_seconds = end_time - start_time
            duration_minutes = duration_seconds / 60

            if duration_seconds < 30:
                wait_long = random.randint(20, 40)
                logger.info(f"Duration is less than 30 seconds. Waiting for {wait_long:.2f} seconds before proceeding.")
                time.sleep(wait_long)
            else:
                wait_short = random.randint(5, 8)
                time.sleep(wait_short)

            payload = {'parameter_name': 'duration', 'parameter_value': round(duration_seconds)}
            headers = {'Content-Type': 'application/json'}
            try:
                response = requests.post(update_parameter_url, json=payload, headers=headers)

                if response.status_code != 200:
                    logger.error("Failed to update duration parameter on master server")
            except Exception as e:
                logger.error(f"Failed to send duration update: {e}")

            logger.info(
                f"🏁 Process completed (ID: {process_id}) - Duration: {duration_minutes:.2f} min, "
                f"Search pages scraped: {nrSearchQueries}, Found events: {nrFoundEventsChecked}, "
                f"Final ticket pages scraped: {nrFinalTicketPageChecked}, Notifications sent: {notifSent}"
            )
            log_resource_usage()

    sys.exit(0)  # Exit with zero status code to indicate success

if __name__ == "__main__":
    main()