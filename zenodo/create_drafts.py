import requests
import os

import requests
import os

import requests
import os

# Your Zenodo API token
access_token = ''

def create_zenodo_draft_record_v4(title, description, authors, file_paths):
    base_url = 'https://sandbox.zenodo.org/api'
    
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    # Step 1: Create a new deposition (draft)
    r = session.post(f'{base_url}/deposit/depositions', json={})
    if r.status_code != 201:
        raise Exception(f"Failed to create deposition: {r.status_code}, {r.text}")
    
    deposition_id = r.json()['id']

    # Step 2: Upload files
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            filename = os.path.basename(file_path)
            files = {'file': (filename, file, 'application/octet-stream')}
            r = session.post(f'{base_url}/deposit/depositions/{deposition_id}/files',
                             files=files)
            if r.status_code != 201:
                raise Exception(f"Failed to upload file {filename}: {r.status_code}, {r.text}")

    # Step 3: Add metadata, including the community
    metadata = {
        'metadata': {
            'title': title,
            'description': description,
            'upload_type': 'dataset',
            'creators': [{'name': author} for author in authors],
            'communities': [{'identifier': 'sandbox-lovers'}],
            'prereserve_doi': True  # This is key for reserving a DOI
        }
    }
    
    r = session.put(f'{base_url}/deposit/depositions/{deposition_id}', json=metadata)
    if r.status_code != 200:
        raise Exception(f"Failed to add metadata: {r.status_code}, {r.text}")

    # Extract and return the reserved DOI
    reserved_doi = r.json()['metadata'].get('prereserve_doi', {}).get('doi')
    if not reserved_doi:
        raise Exception("Failed to reserve DOI")

    return reserved_doi

def create_zenodo_record_v3(title, description, authors, file_paths):
    base_url = 'https://sandbox.zenodo.org/api'
    
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    # Step 1: Create a new deposition
    r = session.post(f'{base_url}/deposit/depositions', json={})
    if r.status_code != 201:
        raise Exception(f"Failed to create deposition: {r.status_code}, {r.text}")
    
    deposition_id = r.json()['id']

    # Step 2: Upload files
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            filename = os.path.basename(file_path)
            files = {'file': (filename, file, 'application/octet-stream')}
            r = session.post(f'{base_url}/deposit/depositions/{deposition_id}/files',
                             files=files)
            if r.status_code != 201:
                raise Exception(f"Failed to upload file {filename}: {r.status_code}, {r.text}")

    # Step 3: Add metadata, including the community
    metadata = {
        'metadata': {
            'title': title,
            'description': description,
            'upload_type': 'dataset',
            'creators': [{'name': author} for author in authors],
            'communities': [{'identifier': 'sandbox-lovers'}]
        }
    }
    
    r = session.put(f'{base_url}/deposit/depositions/{deposition_id}', json=metadata)
    if r.status_code != 200:
        raise Exception(f"Failed to add metadata: {r.status_code}, {r.text}")

    # Step 4: Reserve DOI
    r = session.post(f'{base_url}/deposit/depositions/{deposition_id}/actions/newversion')
    if r.status_code != 201:
        raise Exception(f"Failed to reserve DOI: {r.status_code}, {r.text}")

    # Extract and return the reserved DOI
    return r.json()['doi']

def create_zenodo_record_csrf(title, description, authors, file_paths):
    base_url = 'https://sandbox.zenodo.org/api'

    
    # Start a session to maintain cookies
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    })

    # Step 1: Get CSRF token
    r = session.get(f'{base_url}/deposit/depositions')
    if r.status_code != 200:
        raise Exception(f"Failed to get CSRF token: {r.status_code}, {r.text}")

    # Step 2: Create a new deposition
    r = session.post(f'{base_url}/deposit/depositions', json={})
    if r.status_code != 201:
        raise Exception(f"Failed to create deposition: {r.status_code}, {r.text}")
    
    deposition_id = r.json()['id']

    # Step 3: Upload files
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            filename = os.path.basename(file_path)
            data = {'name': filename}
            files = {'file': file}
            r = session.post(f'{base_url}/deposit/depositions/{deposition_id}/files',
                             data=data,
                             files=files)
            if r.status_code != 201:
                raise Exception(f"Failed to upload file {filename}: {r.status_code}, {r.text}")

    # Step 4: Add metadata, including the community
    metadata = {
        'metadata': {
            'title': title,
            'description': description,
            'upload_type': 'dataset',
            'creators': [{'name': author} for author in authors],
            'communities': [{'identifier': 'sandbox-lovers'}]
        }
    }
    
    r = session.put(f'{base_url}/deposit/depositions/{deposition_id}', json=metadata)
    if r.status_code != 200:
        raise Exception(f"Failed to add metadata: {r.status_code}, {r.text}")

    # Step 5: Reserve DOI
    r = session.post(f'{base_url}/deposit/depositions/{deposition_id}/actions/newversion')
    if r.status_code != 201:
        raise Exception(f"Failed to reserve DOI: {r.status_code}, {r.text}")

    # Extract and return the reserved DOI
    return r.json()['doi']

def create_zenodo_record(title, description, authors, file_paths):
    # Zenodo API base URL
    base_url = 'https://sandbox.zenodo.org/api'
    

    
    # Headers for API requests
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Step 1: Create a new deposition
    r = requests.post(f'{base_url}/deposit/depositions', json={}, headers=headers)
    if r.status_code != 201:
        raise Exception(f"Failed to create deposition: {r.json()}")
    
    deposition_id = r.json()['id']
    bucket_url = r.json()["links"]["bucket"]
    
    # Step 2: Upload files
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            filename = os.path.basename(file_path)
            # Add Referer header for file upload
            upload_headers = {
                "Content-Type": "application/octet-stream",
                "Referer": "https://sandbox.zenodo.org"
            }
            r = requests.put(
                f'{bucket_url}/{filename}',
                data=file,
                headers=upload_headers
            )
        if r.status_code != 200:
            raise Exception(f"Failed to upload file {filename}: {r.json()}")
    
    # Step 3: Add metadata, including the community
    metadata = {
        'metadata': {
            'title': title,
            'description': description,
            'upload_type': 'dataset',
            'creators': [{'name': author} for author in authors],
            'communities': [{'identifier': 'sandbox-lovers'}]
        }
    }
    
    r = requests.put(f'{base_url}/deposit/depositions/{deposition_id}', json=metadata, headers=headers)
    if r.status_code != 200:
        raise Exception(f"Failed to add metadata: {r.json()}")
    
    # Step 4: Reserve DOI
    r = requests.post(f'{base_url}/deposit/depositions/{deposition_id}/actions/newversion', headers=headers)
    if r.status_code != 201:
        raise Exception(f"Failed to reserve DOI: {r.json()}")
    
    # Extract and return the reserved DOI
    return r.json()['doi']

def create_zenodo_draft_record(title, description, authors, file_paths):
    base_url = 'https://sandbox.zenodo.org/api'
    
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    # Step 1: Create a new deposition (draft)
    r = session.post(f'{base_url}/deposit/depositions', json={})
    if r.status_code != 201:
        raise Exception(f"Failed to create deposition: {r.status_code}, {r.text}")
    
    deposition_id = r.json()['id']

    # Step 2: Upload files
    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            filename = os.path.basename(file_path)
            files = {'file': (filename, file, 'application/octet-stream')}
            r = session.post(f'{base_url}/deposit/depositions/{deposition_id}/files',
                             files=files)
            if r.status_code != 201:
                raise Exception(f"Failed to upload file {filename}: {r.status_code}, {r.text}")

    # Step 3: Add metadata, including the community and authors with ORCID
    metadata = {
        'metadata': {
            'title': title,
            'description': description,
            'upload_type': 'dataset',
            'creators': authors,  # Now passing the full author structure
            'communities': [{'identifier': 'sandbox-lovers'}],
            'prereserve_doi': True
        }
    }
    
    r = session.put(f'{base_url}/deposit/depositions/{deposition_id}', json=metadata)
    if r.status_code != 200:
        raise Exception(f"Failed to add metadata: {r.status_code}, {r.text}")

    # Extract and return the reserved DOI
    reserved_doi = r.json()['metadata'].get('prereserve_doi', {}).get('doi')
    if not reserved_doi:
        raise Exception("Failed to reserve DOI")

    return reserved_doi

# Example usage
titles = ["dodoid"]
description = "This is a sample description for the record."
authors = [
    {
        "name": "Clunie, David",
        "orcid": "0000-0002-2406-1145"  # Replace with actual ORCID
    },
    {
        "name": "Doe, Jane",
        "orcid": "0000-0001-9876-5432"  # Replace with actual ORCID
    }
]
file_paths = ["/Users/af61/Downloads/total.csv"]

dois = []

for title in titles:
    try:
        doi = create_zenodo_draft_record(title, description, authors, file_paths)
        dois.append(doi)
        print(f"Created draft record '{title}' with reserved DOI: {doi}")
    except Exception as e:
        print(f"Error creating record '{title}': {str(e)}")

print("Reserved DOIs:", dois)
