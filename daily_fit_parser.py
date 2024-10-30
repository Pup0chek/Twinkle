import os
import requests
import openpyxl
from bs4 import BeautifulSoup
import chardet
from lxml import html
import pandas as pd

# Base URL of the exercise catalog
base_url = 'https://dailyfit.ru/katalog-uprazhnenij/'

# Output file for Excel
output_file = "exercises_data.xlsx"

# Initialize an empty list to hold data for all exercises
exercises_data = []

# Loop through pages
for i in range(1, 31):
    # Fetch each page
    url = f'{base_url}?pg={i}'
    response = requests.get(url)

    # Check if the page request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate exercise cards
        exercise_cards = soup.find_all('div', class_='ui fluid card')

        for card in exercise_cards:
            # Extract exercise name and link
            header = card.find('a', class_='header')
            header_text = header.text.strip().encode()
            detected_encoding = chardet.detect(header_text)['encoding']
            try:
                exercise_name = html.document_fromstring(header_text.decode(detected_encoding)).text_content()
            except Exception as e:
                print(f"Ошибка декодирования для упражнения '{header.text.strip()}': {e}")
                exercise_name = "Ошибка декодирования имени"
            exercise_link = header['href']

            response = requests.get(exercise_link)
            if response.status_code == 200:
                exercise_soup = BeautifulSoup(response.content, 'html.parser')

                # Find and construct description list for each exercise
                description_items = exercise_soup.find('h4', class_='ui header').find_next('ol')
                description = [li.text.strip() for li in description_items.find_all('li')] if description_items else []
                description_text = "; ".join(description)  # Join descriptions into a single string

                # Extract additional details (muscle group, equipment, difficulty)
                description_items = card.find('div', class_='description').find_all('div', class_='item')
                muscle_group, equipment, difficulty = "", "", ""

                for item in description_items:
                    item_text = item.text.strip()
                    if 'Группа мышц:' in item_text:
                        muscle_group = item_text.split('Группа мышц:')[1].strip()
                    elif 'Оборудование:' in item_text:
                        equipment = item_text.split('Оборудование:')[1].strip()
                    elif 'Уровень сложности:' in item_text:
                        difficulty = item_text.split('Уровень сложности:')[1].strip()

                # Append extracted exercise data to the list
                exercises_data.append({
                    'Name': exercise_name,
                    'Link': exercise_link,
                    'Muscle Group': muscle_group,
                    'Equipment': equipment,
                    'Difficulty': difficulty,
                    'Description': description_text
                })

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Convert the data to a pandas DataFrame
df = pd.DataFrame(exercises_data)

# Write the DataFrame to an Excel file (без encoding)
df.to_excel(output_file, index=False)
print(f"Data successfully written to {output_file}")
