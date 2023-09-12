# Author: Binh Lam
# Contact: binh.lam@global.ntt
# Description: This script retrieves JSON data from the Shodan API for a list of IP addresses,
# converts it into a table format, and writes the 

import requests
import json
import csv
import sys

# Function to retrieve JSON data for an IP address
def get_host_data(ip_address):
    # Construct the URL for the Shodan API with the IP address
    url = f"https://internetdb.shodan.io/{ip_address}"
    
    # Send a GET request to retrieve the JSON data
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON data as a Python dictionary
        return response.json()
    else:
        # Return None if the request failed
        return None

# Function to convert JSON data into a table format
def save_to_table(data):
    table = []
    # Iterate through the key-value pairs in the data dictionary
    for key, value in data.items():
        # Check if the value is a list
        if isinstance(value, list):
            # Convert the list values to a comma-separated string
            value = ', '.join(str(v) for v in value)
        
        # Append the key-value pair as a list to the table
        table.append([key, str(value)])
    
    return table

# Read IP addresses from the text file
filename = sys.argv[1]  # Read file name from command line argument
with open(filename, 'r') as file:
    ip_addresses = [ip.strip() for ip in file.read().splitlines()]

# Process each unique IP address
unique_ip_addresses = set(ip_addresses)
results = []
for ip_address in unique_ip_addresses:
    # Retrieve the JSON data for the IP address
    host_data = get_host_data(ip_address)
    if host_data is not None:
        try:
            # Convert the JSON data into a table format
            table_data = save_to_table(host_data)
            
            # Create a result dictionary with the IP address
            result = {"IP": ip_address}
            
            # Iterate through the table data and add it to the result
            for row in table_data:
                result[row[0]] = row[1]
            
            # Append the result to the list of results
            results.append(result)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON data for IP: {ip_address}")
    else:
        print(f"Failed to retrieve data for IP: {ip_address}")

# Write results to a CSV file
output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.csv'  # Read output file name from command line argument, or default to 'output.csv'
with open(output_file, 'w', newline='') as file:
    # Create a CSV writer and specify the fieldnames
    writer = csv.DictWriter(file, fieldnames=["IP"] + [row[0] for row in table_data])
    
    # Write the header row
    writer.writeheader()
    
    # Write the rows of data
    writer.writerows(results)
print("Process completed successfully.")

