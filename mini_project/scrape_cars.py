import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL of the website
website = "https://www.cars24.com/buy-used-car?f=make%3A%3D%3Atata&sort=bestmatch&serveWarrantyCount=true&gaId=2081209776.1722768914&listingSource=TabFilter&storeCityId=2378"

# Send a request to fetch the HTML content
response = requests.get(website)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the car details containers
    results = soup.find_all("div", {"class": "_2YB7p"})

    # Initialize lists to store the extracted data
    car_makes = []
    car_models = []
    kilometers_driven = []
    fuel_types = []
    transmission_types = []
    car_prices = []
    locations = []

    # Extract data from the results
    for result in results:
        # Extract car name and price
        name = result.find("h3").get_text() if result.find("h3") else "N/A"
        price = result.find("strong").get_text() if result.find("strong") else "N/A"
        
        # Extract make and model from car name
        name_parts = name.split(' ', 1)
        make = name_parts[0] if len(name_parts) > 1 else "N/A"
        model = name_parts[1] if len(name_parts) > 1 else "N/A"
        
        # Extract details from the <ul> element
        ul_element = result.find("ul", {'class': '_3J2G-'})
        if ul_element:
            list_items = ul_element.find_all("li")
            details = [item.get_text(strip=True) for item in list_items if item.get_text(strip=True)]
            
            # Extract specific details from the list items
            km_driven = details[0] if len(details) > 0 else "N/A"
            fuel_type = details[1] if len(details) > 1 else "N/A"
            transmission = details[2] if len(details) > 2 else "N/A"
        else:
            km_driven = "N/A"
            fuel_type = "N/A"
            transmission = "N/A"

        # Extract location information
        para_element=result.find("p",{'class':'_3dGMY'})
        if para_element:
            location=para_element.get_text()
            words=location.split()
            words=words[-2:]
            location=','.join(words)
        else:
            location="N/A"
        # Append the extracted information to lists
        car_makes.append(make)
        car_models.append(model)
        kilometers_driven.append(km_driven)
        fuel_types.append(fuel_type)
        transmission_types.append(transmission)
        car_prices.append(price)
        locations.append(location)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({
        'Car Make': car_makes,
        'Car Model': car_models,
        'Kilometers Driven': kilometers_driven,
        'Fuel Type': fuel_types,
        'Transmission Type': transmission_types,
        'Price': car_prices,
        'Location': locations
    })

    # Save the DataFrame to a CSV file
    df.to_csv('cars24_data.csv', index=False)
    print("Data has been saved to 'cars24_data.csv'")
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")
