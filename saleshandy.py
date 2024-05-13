# Import necessary libraries
import requests  #  send HTTP requests
import json      #  work with JSON data
import os        #  interact with the operating system
import time      #  time-related operations like adding delays

# this function is used  to send HTTP requests and validate the respected responses
def test_endpoint(endpoint_config):
    try:
        # Extract request details from endpoint configuration
        request_method = endpoint_config['request']['method']  # Extracts the http request method
        request_url = endpoint_config['request']['url']        # Extracts the URL for the API request
        payload = endpoint_config['request'].get('payload')    # Extracts the payload data
    except KeyError as e:
        print(f"Error: Key '{e}' not found in endpoint configuration")
    # Sending HTTP request
    try:
        if request_method.lower() == 'get':
            response = requests.get(request_url)               # will send a GET request
        elif request_method.lower() == 'post':
            response = requests.post(request_url, json=payload) # will Send a POST request with JSON body
        elif request_method.lower() == 'put':
            response = requests.put(request_url, json=payload)  # will Send a put request with JSON body
        elif request_method.lower() == 'patch':
            response = requests.patch(request_url, json=payload)  # will Send a patch request with JSON body

    except requests.exceptions.RequestException as e:
        print(f"Error occuring dusing Following HTTP request : {e}")
        return None

    # will put assertions
    test_results = {}
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
    # will Return test result
    test_results['url']=request_url,
    test_results['method'] = request_method,
    test_results['status_code']=response.status_code,
    test_results['response_time_ms']=response.elapsed.total_seconds() * 1000
    return test_results


# this is the main function to execute tests for all endpoints
def main():
    # this directory containing endpoint configurations
    endpoints_directory = 'endpoints/'

    # will create a dictionary to store test results
    test_results = {}

    # will iterate through each JSON file in the endpoints directory
    for file_name in os.listdir(endpoints_directory):
        if file_name.endswith('.json'):
            with open(os.path.join(endpoints_directory, file_name), 'r') as file:
                endpoint_config = json.load(file)               # Loads the JSON configuration for the endpoint
                test_result = test_endpoint(endpoint_config)   # Calls the test_endpoint function to test the endpoint
                test_results[file_name] = test_result          # Stores the test result in a dictionary
                time.sleep(1)  # Adding a small delay between tests to avoid error on the server

    # will log test results
    with open('test_results.json', 'w') as results_file:
        json.dump(test_results, results_file, indent=4 )      # Writes the test results to a JSON file

    # Print message
    print("API tests are completed.")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
