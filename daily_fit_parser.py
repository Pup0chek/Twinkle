import os
import psycopg2
import requests
from bs4 import BeautifulSoup

# Base URL of the exercise catalog
base_url = 'https://dailyfit.ru/katalog-uprazhnenij/'

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Almaty111@db:5432/lol").encode('utf-8').decode('utf-8')

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

        # Initialize a list to hold data for all exercises
        exercises = []

        for card in exercise_cards:
            # Extract exercise name and link
            header = card.find('a', class_='header')
            exercise_name = header.text.strip()
            exercise_link = header['href']

            # Fetch individual exercise page
            response = requests.get(exercise_link)
            if response.status_code == 200:
                exercise_soup = BeautifulSoup(response.content, 'html.parser')

                # Find and construct description list for each exercise
                description_items = exercise_soup.find('h4', class_='ui header').find_next('ol')
                description = [li.text.strip() for li in description_items.find_all('li')] if description_items else []

                # Extract image URL if available
                image_tag = exercise_soup.find('img', class_='ui centered image')
                image_url = "https://dailyfit.ru/" + image_tag['src'] if image_tag else None

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

                # Append extracted exercise data
                exercises.append({
                    'name': exercise_name,
                    'link': exercise_link,
                    'description': description,
                    'image_url': image_url,
                    'muscle_group': muscle_group,
                    'equipment': equipment,
                    'difficulty': difficulty
                })

        # Print or return the extracted data
        for exercise in exercises:
            connection = None
            cursor = None
            try:
                # Establish connection with UTF-8 encoding explicitly set
                connection = psycopg2.connect(DATABASE_URL)
                connection.set_client_encoding('UTF8')
                cursor = connection.cursor()

                insert_query = """
                    INSERT INTO exercises (name, description, muscle_group, equipment, difficulty)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    exercise['name'],
                    str(exercise['description']),
                    exercise['muscle_group'],
                    exercise['equipment'],
                    exercise['difficulty']
                ))

                connection.commit()
                print(f"Inserted: {exercise['name']}")

            except UnicodeDecodeError as e:
                print(f"Encoding error with exercise '{exercise['name']}': {e}")
            except Exception as db_error:
                print(f"Database error with exercise '{exercise['name']}': {db_error}")

            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
