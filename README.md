
# TICKET SCRAPER Project Architecture

## Overview

This system is architected with a **master server** and multiple **node servers** to ensure scalability and efficient processing. The master server manages the frontend application, backend scraping for search functionalities, event generation, and data storage. Multiple node servers handle the processing of events by performing scraping tasks on various web pages. Future enhancements include implementing an auto-scaling group for the node servers based on the volume of pending events, monitored via CloudWatch.

## Architecture Components

### Master Server

- **Frontend Application**: Hosts the user interface, allowing users to interact with the system.
- **Backend Scraper**: Dedicated to handling search-related scraping operations.
- **Event Generation**: Produces events that need to be processed and publishes them to an Amazon SQS (Simple Queue Service) queue.
- **Database Hosting**: Runs MongoDB to manage and store:
  - User data
  - Tracked ticket data
  - Additional application-specific information

### Node Servers

- **Event Processing**: Consume and process events from the SQS queue.
- **Scraping Operations**: Perform scraping tasks on various target web pages based on the events received.

## Event Queue

- **Amazon SQS**: Acts as the messaging queue where the master server publishes events. Node servers subscribe to this queue to retrieve and process events.

## Future Enhancements

- **Auto-Scaling Node Servers**:
  - **Implementation**: Establish an auto-scaling group for node servers to dynamically adjust the number of active nodes based on the number of pending events in the SQS queue.
  - **Monitoring**: Use Amazon CloudWatch to track the queue length and trigger scaling actions accordingly, ensuring optimal resource utilization and performance.


## Technologies Used

- **Frontend**: [React Next.js]
- **Backend**: [Node.js, Python, Nginx, FlaskApp]
- **Database**: MongoDB
- **Queue Service**: Amazon SQS
- **Monitoring**: Amazon CloudWatch
- **Hosting**: [AWS EC2 t3a.small for master, t3.medium for nodes]




# THIS IS THE REPO FOR THE NODE SERVER:

### PIP LIBRARIES GLOBAL INSTALLATION:
sudo apt install python3-(libraryname)

Using apt to install Python packages is beneficial in environments where system stability is critical, and you want to avoid conflicts between packages managed by pip and the system's package manager. However, this approach might not give you the most recent version of the package compared to installing via pip.

If you need the latest version or need more control over your Python environment, consider using a virtual environment as previously described. For system-wide installations that align with Ubuntu's package management policies, using apt is a suitable choice.

Verify the Installation: After installation, you can verify that pymongo was installed correctly by opening a Python shell and importing pymongo:
python3
import pymongo
print(pymongo.__version__)

installed python packages globally:
sudo apt install python3-flask python3-selenium python3-bs4 python3-chromium-browser  python3-chromium-chromedriver



### scraper.py execution mode:

1) WITH CRON (default)
* * * * * /home/ubuntu/ticket-scraper/backend/run_scraper.sh



2) WITH SERVICE

sudo nano /etc/systemd/system/scrape.service

Add the following configuration to the service file:

[Unit]
Description=Scraper
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/ubuntu/ticket-scraper/backend/scrape.py
WorkingDirectory=/home/ubuntu/ticket-scraper/backend
Restart=always
RestartSec=10
User=ubuntu
Environment=PYTHONUNBUFFERED=1
StandardOutput=append:/home/ubuntu/ticket-scraper/backend/logs/scrape_service.log
StandardError=append:/home/ubuntu/ticket-scraper/backend/logs/scrape_service-error.log

[Install]
WantedBy=multi-user.target

some command to manage the service:
sudo systemctl stop scrape.service
sudo systemctl start scrape.service
sudo systemctl enable scrape.service
sudo systemctl status scrape.service
sudo systemctl daemon-reload 
sudo systemctl restart scrape.service





# SCRAPER SCRIPT

## **Overview**

The Ticket Scraper is a sophisticated Python-based tool designed to monitor and extract ticket availability from [Fansale.it](https://www.fansale.it). Leveraging Selenium with `undetected_chromedriver`, the scraper bypasses common anti-scraping mechanisms and employs various strategies to mimic human behavior, ensuring effective and stealthy data extraction.

## **Key Features**

1. **Logging and Configuration:**
   - Utilizes Python's `logging` module with a `RotatingFileHandler` to efficiently manage log files, logging files in: /home/ubuntu/ticket-scraper/backend/logs
   - Configures essential URLs and file paths for logging and parameter updates.

2. **Proxy and User-Agent Management:**
   - Maintains a list of proxies to rotate IP addresses, reducing the risk of IP bans.
   - Randomly selects user-agent strings from a predefined list to mimic different browsers and devices.

3. **Browser Automation:**
   - Uses `undetected_chromedriver` to initiate a Chromium browser instance that avoids detection by anti-bot mechanisms.
   - Configures browser options to disable automation flags, set language preferences, and manage proxy settings.
   - Implements a virtual display with `pyvirtualdisplay` to run the browser in headless mode.

4. **Scraping Logic:**
   - Retrieves messages from an SQS queue containing ticket tracking information.
   - For each unique event, navigates to the event's ticket page, simulates user interactions (mouse movements and scrolling) to appear human-like, and extracts ticket availability.
   - Detects anti-scraping measures by checking the presence of specific HTML elements and updates a master server if scraping is detected.
   - Matches available tickets with user requirements and sends notifications accordingly.

5. **Resource and Process Management:**
   - Implements a lock mechanism to prevent multiple instances from running simultaneously.
   - Monitors and logs CPU and memory usage to ensure efficient resource utilization.
   - Handles signals gracefully to release locks and terminate processes safely.

6. **Error Handling and Cleanup:**
   - Incorporates extensive try-except blocks to capture and log errors without crashing.
   - Cleans up temporary files and browser instances to maintain system stability.
   - Collects garbage to free up memory after intensive operations.

7. **Execution Flow:**
   - The `main` function orchestrates the entire scraping process, from acquiring locks and fetching messages to processing events and sending notifications.
   - Ensures the script exits gracefully, logging the duration and resource usage upon completion.

## **Anti-Scraping Measures Employed**

1. **Undetected Chromedriver:**
   - Utilizes `undetected_chromedriver` to evade detection by websites that identify and block automated browser instances.

2. **Proxy Rotation:**
   - Implements a pool of proxies, randomly selecting one for each session to mask the scraper's IP address and distribute requests.

3. **Random User-Agent Selection:**
   - Randomly chooses user-agent strings from a diverse list to simulate requests from different browsers and devices, reducing the likelihood of detection.

4. **Navigator Property Spoofing:**
   - Alters browser navigator properties such as `webdriver`, `deviceMemory`, `hardwareConcurrency`, and `platform` to mimic genuine user environments.
   - Overrides the `HTMLCanvasElement.prototype.toDataURL` method to prevent canvas fingerprinting.

5. **Simulated User Interactions:**
   - Performs human-like actions such as mouse movements and scrolling to emulate real user behavior, making automation less detectable.

6. **Headless Browsing with Virtual Display:**
   - Runs the browser in headless mode using `pyvirtualdisplay`, which can help in avoiding headless browser detection techniques.

7. **Browser Options Configuration:**
   - Disables automation flags (`--disable-blink-features=AutomationControlled`) and other features that could signal automated browsing.
   - Sets language preferences and window sizes to standardize the browsing environment.

8. **Temporary User Profiles:**
   - Uses temporary directories for user data to prevent persistent profiles that could be tracked or flagged.

9. **Error Handling and Recovery:**
   - Monitors for signs of scraping detection (e.g., missing HTML elements) and updates the master server to adjust scraping parameters accordingly.

10. **Resource Management:**
    - Regularly logs and manages CPU and memory usage to maintain optimal performance and avoid resource leaks that could raise red flags.

11. **Process and Temporary File Cleanup:**
    - Ensures that all Chromium processes and temporary files are terminated and removed after each scraping session to prevent residual traces.

By integrating these measures, the script effectively minimizes the risk of detection and blocking by target websites, ensuring continuous and reliable scraping operations.

## **Compatibility and Additional Notes**

### **Compatibility Between `undetected_chromedriver`, Chromium, and ChromeDriver Versions**

- **Version Compatibility:**
  - It is crucial to periodically verify that there are no incompatibilities between `undetected_chromedriver`, Chromium, and ChromeDriver versions, especially since Snap automatically updates Chrome versions.
  
- **Package Updates:**
  - Regularly update the `undetected_chromedriver` package to prevent the scraping site from recognizing the bot and blocking access.
  - Ensure compatibility with new versions of Chrome and ChromeDriver to maintain seamless operation.
  
- **Snapshot Precautions:**
  - **Important:** Before updating `undetected_chromedriver`, create an AWS snapshot of the previous version. This allows you to revert to the previous state in case of any issues post-update.

- **Additional Information:**
  - For more details on `undetected-chromedriver`, visit the [undetected-chromedriver GitHub repository](https://github.com/ultrafunkamsterdam/undetected-chromedriver).

### **Virtual Display**

- **Usage on Servers:**
  - **Note:** `webdriver.Chrome` operates only on PCs. On servers, it is necessary to initiate `pyvirtualdisplay` to create a virtual display environment.
  - Refer to [this StackOverflow thread](https://stackoverflow.com/questions/28119570/how-to-make-selenium-and-chromium-work-on-ubuntu) for guidance on setting up `pyvirtualdisplay` with Selenium and Chromium on Ubuntu.

- **Installation Considerations:**
  - A virtual environment was created exclusively for `pyvirtualdisplay` because it cannot be installed globally.

By adhering to these compatibility guidelines and setup instructions, you can ensure that the scraping script remains functional and resilient against updates or changes in dependencies.




