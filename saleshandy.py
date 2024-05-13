import requests
import json
import os
import time


# Function to send HTTP requests and validate responses
def test_endpoint(endpoint_config):
    # Extract request details from endpoint configuration
    request_method = endpoint_config['request']['method']
    request_url = endpoint_config['request']['url']
    payload = endpoint_config['request'].get('payload')

    # Send HTTP request
    if request_method.lower() == 'get':
        response = requests.get(request_url)
    elif request_method.lower() == 'post':
        response = requests.post(request_url, json=payload)

    # Assertions
    assert response.status_code == endpoint_config['assertions']['responseCode'], \
        f"Expected status code {endpoint_config['assertions']['responseCode']}, but got {response.status_code}"
    assert endpoint_config['assertions']['content-type'] in response.headers['Content-Type'], \
        f"Expected content type {endpoint_config['assertions']['content-type']}, but got {response.headers['Content-Type']}"

    # Check if 'maxResponseTimeInMilliseconds' key exists in assertions dictionary
    if 'maxResponseTimeInMilliseconds' in endpoint_config['assertions']:
        assert response.elapsed.total_seconds() * 1000 <= endpoint_config['assertions'][
            'maxResponseTimeInMilliseconds'], \
            f"Response time exceeded maximum allowed time ({endpoint_config['assertions']['maxResponseTimeInMilliseconds']} ms)"

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
                endpoint_config = json.load(file)
                test_result = test_endpoint(endpoint_config)
                test_results[file_name] = test_result
                time.sleep(1)  # Adding a small delay between tests

    # Log test results
    with open('test_results.json', 'w') as results_file:
        json.dump(test_results, results_file, indent=4)

    print("API tests completed. Test results have been logged.")


if __name__ == "__main__":
    main()
