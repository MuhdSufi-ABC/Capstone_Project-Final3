import requests
import json

# URL for SSG API (example URL, update as needed)
api_url = "https://api.ssg-wsg.sg/courses"
params = {
    'keyword': 'digital',
    'limit': 500
}
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY_HERE'  # Replace with your API key
}

# File name to save the fetched data
json_file_name = 'skillsfuture_courses.json'

try:
    # Fetch data from API
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    courses_data = response.json()

    # Save data to local JSON file
    with open(json_file_name, 'w') as json_file:
        json.dump(courses_data, json_file)

    print('Courses fetched successfully and saved to', json_file_name)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")