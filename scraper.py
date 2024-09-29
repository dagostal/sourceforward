import requests
import logging
import json
from scrape_incentive import get_incentives

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():    
    api_url = "https://programs.dsireusa.org/api/v1/programs?state[]=24&&draw=1&columns%5B0%5D%5Bdata%5D=name&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B1%5D%5Bdata%5D=stateObj.abbreviation&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B2%5D%5Bdata%5D=categoryObj.name&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B3%5D%5Bdata%5D=typeObj.name&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B4%5D%5Bdata%5D=published&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B5%5D%5Bdata%5D=createdTs&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B6%5D%5Bdata%5D=updatedTs&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&order%5B0%5D%5Bcolumn%5D=6&order%5B0%5D%5Bdir%5D=desc&start=0&length=50&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1727576565224"

    response = requests.get(api_url)

    if response.status_code == 200:
        try:
            json_data = response.json()
            list_of_programs_on_page = json_data["data"]
            results = []  # List to hold all the incentive data
           
            for incentive in list_of_programs_on_page:
                obj_modal = {}
                incentive_name = incentive["name"].lower().replace(" ","")
                incentive_id = incentive["id"]                
                if incentive_name == "delmarva-evsmart":
                    for key, value in incentive.items():                
                        obj_modal[key] = value
                    incentive_url = "https://programs.dsireusa.org/system/program/detail/" + str(incentive_id) + "/" + incentive_name
                    incentive_data = get_incentives(incentive_url)
                    for key,value in incentive_data.items():
                        obj_modal[key] = value
                    results.append(obj_modal)  # Collect the result
           
            print(json.dumps(results))  # Print the results as JSON
           
        except ValueError as e:
            print("Error decoding JSON:", e)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
