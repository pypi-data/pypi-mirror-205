import requests

url = "http://127.0.0.1:5000/predict"

print("Enter your input and press Enter to send a POST request to the Flask backend.")
print("Press Ctrl+C to exit.\n")

while True:
    try:
        user_input = input("Input: ")

        payload = {{input_key}: user_input}

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("Answer: ", response.json()[{output_key}])
        else:
            print("Request failed with status code:", response.status_code)

    except KeyboardInterrupt:
        print("\nExiting the program.")
        break
