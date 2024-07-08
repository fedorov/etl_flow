import requests

def test_zenodo_api():
    base_url = 'https://sandbox.zenodo.org/api'  # or 'https://sandbox.zenodo.org/api' for testing
    access_token = ''
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Create a new deposition
    r = requests.post(f'{base_url}/deposit/depositions', json={}, headers=headers)
    if r.status_code != 201:
        print(f"Failed to create deposition: {r.status_code}")
        print(r.text)
    else:
        print("Successfully created deposition")
        print(r.json())

test_zenodo_api()
