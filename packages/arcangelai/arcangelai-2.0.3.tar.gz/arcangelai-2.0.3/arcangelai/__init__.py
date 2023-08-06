import requests

class Arc:
    def __init__(self, props):
        self.key = props['key']
        self.name = props['name']

    def chat(self, user_input):
        # Define the API endpoint URL
        url = 'http://54.166.81.208/v2/arc'

        # Set the API key in the header
        headers = {'X-API-KEY': self.key}

        # Set the message in the body as a JSON object
        data = {'message': user_input}

        # Make the API post request
        response = requests.post(url, headers=headers, json=data)

        # Check if the API call was successful
        if response.status_code == 200:
            # Get the JSON response
            json_response = response.json()
            return json_response
        else:
            # Handle the error
            return response
