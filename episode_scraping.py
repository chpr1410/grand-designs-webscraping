from selenium import webdriver
from time import sleep
import pandas as pd
from tqdm import tqdm

# Initialize Webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

#  Go to Show's Page
url = 'https://www.channel4.com/programmes/grand-designs'
driver.get(url)
sleep(2)

# Don't Accept Cookies
roadblock_button = driver.find_element_by_class_name('all4-cc-secondary-button.all4-cc-typography-body.false.row-margin-sm-0.row-margin-md-0.row-margin-lg-0.col-xs-1-12.col-sm-1-6.col-md-1-6.col-lg-1-6')
roadblock_button.click()
sleep(2)

roadblock_button_2 = driver.find_element_by_class_name("all4-cc-secondary-button.all4-cc-typography-body.col-xs-1-12.col-sm-1-6.col-md-1-6.col-lg-1-6")
roadblock_button_2.click()
sleep(2)

# Load All Episodes
all_episodes_showing = False

while not all_episodes_showing:
    try:
        show_more_button = driver.find_element_by_class_name('all4-secondary-button.all4-typography-body.all4-episode-list__button')
        show_more_button.click()
    except:
        all_episodes_showing = True
        
# Get Episode Info and Save in DF

episode_containers = driver.find_elements_by_class_name("all4-episode-list-item.all4-episode-list__container-list-item")

episode_urls = []
episode_titles = []
episdoe_descriptions = []
episode_years = []
episode_numbers = []
episode_air_dates = []

for container in tqdm(episode_containers):
    episode_url = container.get_attribute('href')
    episode_title = container.find_element_by_class_name("all4-typography-heading3-medium.all4-episode-list-item__title").text
    episdoe_description = container.find_element_by_class_name("all4-body-tight-text-label.all4-typography-body-tight.all4-episode-list-item__description.secondary").text
    
    episode_first_shown = container.find_element_by_class_name("all4-caption-text.all4-typography-caption.all4-episode-list-item__bottom-area-text.secondary.aligned-left").text
    episode_year = int(episode_first_shown.split(' |')[0][-4:])

    episode_air_date = episode_first_shown.split(': ')[1].split(' |')[0]

    episode_number = episode_url.split('https://www.channel4.com/programmes/grand-designs/on-demand/')[1].split('-')[1]
    
    episode_urls.append(episode_url)
    episode_titles.append(episode_title)
    episdoe_descriptions.append(episdoe_description)
    episode_years.append(episode_year)
    episode_numbers.append(episode_number)
    episode_air_dates.append(episode_air_date)
    
df = pd.DataFrame()
df['Year'] = episode_years
df['Number'] = episode_numbers
df['Air Date'] = episode_air_dates
df['Title'] = episode_titles
df['Description'] = episdoe_descriptions
df['URL'] = episode_urls
 
df = df.sort_values(['Year','Number'],ignore_index=True)

# Save result in spreadsheet
df.to_excel('Grand Designs Episode List.xlsx',index=False)