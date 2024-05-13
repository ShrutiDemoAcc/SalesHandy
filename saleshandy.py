# Import necessary libraries
import requests  #  send HTTP requests
import json      #  work with JSON data
import os        #  interact with the operating system
import time      #  time-related operations like adding delays

# Function to send HTTP requests and validate responses
def test_endpoint(endpoint_config):
    # Extract request details from endpoint configuration
    request_method = endpoint_config['request']['method']  # Extracts the request method (GET or POST)
    request_url = endpoint_config['request']['url']        # Extracts the URL for the API request
    payload = endpoint_config['request'].get('payload')    # Extracts the payload data (if it exists)

    # Send HTTP request
    if request_method.lower() == 'get':
        response = requests.get(request_url)               # Sends a GET request
    elif request_method.lower() == 'post':
        response = requests.post(request_url, json=payload) # Sends a POST request with JSON payload

    # Assertions
    for assertion_key, expected_value in endpoint_config['assertions'].items():
        if assertion_key == 'responseCode':
            assert response.status_code == expected_value, \
                f"Expected status code {expected_value}, but got {response.status_code}"
        elif assertion_key == 'content-type':
            assert expected_value in response.headers['Content-Type'], \
                f"Expected content type {expected_value}, but got {response.headers['Content-Type']}"
        elif assertion_key == 'maxResponseTimeInMilliseconds':
            assert response.elapsed.total_seconds() * 1000 <= expected_value, \
                f"Response time exceeded maximum allowed time ({expected_value} ms)"
        else:
            print(f"Warning: Assertion key '{assertion_key}' not found in response JSON.")

    # Return test result
    return {
        'url': request_url,
        'method': request_method,
        'status_code': response.status_code,
        'response_time_ms': response.elapsed.total_seconds() * 1000
    }

# Main function to execute tests for all endpoints
def main():
    # Directory containing endpoint configurations
    endpoints_directory = 'endpoints/'

    # Create a dictionary to store test results
    test_results = {}

    # Iterate through each JSON file in the endpoints directory
    for file_name in os.listdir(endpoints_directory):
        if file_name.endswith('.json'):
            with open(os.path.join(endpoints_directory, file_name), 'r') as file:
                endpoint_config = json.load(file)               # Loads the JSON configuration for the endpoint
                test_result = test_endpoint(endpoint_config)   # Calls the test_endpoint function to test the endpoint
                test_results[file_name] = test_result          # Stores the test result in a dictionary
                time.sleep(1)  # Adding a small delay between tests to avoid overwhelming the server

    # Log test results
    with open('test_results.json', 'w') as results_file:
        json.dump(test_results, results_file, indent=4)       # Writes the test results to a JSON file

    # Print completion message
    print("API tests completed.")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
