import requests
import json
from bs4 import BeautifulSoup




def get_incentives(url):

# Make a GET request to fetch the raw HTML content
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <div> elements with the specific data-ng-controller attribute
        program_details = soup.find_all('div', attrs={'data-ng-controller': 'DetailsPageCtrl'})

        for detail in program_details:
            # Extract the data-ng-init attribute
            ng_init = detail.get('data-ng-init')

            if ng_init:
                # Clean the string: Replace HTML entities and extract the JSON part
                cleaned_ng_init = ng_init.replace('&quot;', '"').replace("init(", "").replace(")", "")
               
                try:
                    # Parse the cleaned string as JSON
                    program_data = json.loads(cleaned_ng_init)
                   
                    program_obj = {}
                    #program["program"]
                    for key,value in program_data["program"].items():
                        program_obj[key] = value                    
                   
                    for key,value in program_data.items():
                        if key == "programs":                        
                            break;
                        program_obj[key] = value                    
           
                    #program -- > everything else!. may need further parsing
                    # for key, value in program_data.items():                
                    #     print(f"{key}: {value}")  # Print the key-value pair
                   
                    # Now you can access the data as a Python dictionary
                    # print("Program ID:", program_data["program"]["id"])
                    # print("Program Name:", program_data["program"]["name"])
                    # print("Summary:", program_data["program"]["summary"])
                    # print("GOT INCENTIVE INFO!")
                    return(program_obj)
                    print("---")

                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
