from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

# Lista degli eventi
eventList = []

# Input della ricerca
searchText = 'flor-bertotti/806779'

# Effettua la ricerca su FanSale
driver.get("https://www.fansale.it/tickets/all/" + searchText)

# Ottieni l'HTML della pagina
html = driver.page_source

# Chiudi il webdriver
driver.quit()

# Analizza l'HTML con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Trova gli elementi con la classe 'ListEntry'
entry_headers = soup.find_all(class_='ListEntry')

# Itera su ogni elemento e ottieni i loro sottoelementi
for header in entry_headers:
    # Ottieni il link
    link = header.get('href')

    # Trova la data dell'evento
    data = header.get('data-tracking-eventdate')

    # Trova il luogo dell'evento
    luogo = header.find(class_='EvEntryRow-highlightedTitle').text.strip()

    # Aggiungi i dettagli dell'evento alla lista degli eventi
    eventList.append([link, data, luogo])

# Stampare la lista degli eventi per verificarne il contenuto
for evento in eventList:
    print(evento)