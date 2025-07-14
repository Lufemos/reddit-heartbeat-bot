import requests


HEARTBEAT_API_KEY = 'hb:483284675f159ed7c7bb016d4f73f06604ad198cde4b600847'
HEARTBEAT_BASE_URL = 'https://guide.heartbeat.chat/threads'  

def post_to_heartbeat(channel_id, content):
    headers = {
        'Authorization': f'Bearer {HEARTBEAT_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'channel_id': channel_id, 
        'content': content          
    }

    response = requests.post(f'{HEARTBEAT_BASE_URL}/messages', json=data, headers=headers)
    
    if response.status_code == 201:
        print(f"Successfully posted to channel {channel_id}")
    else:
        print(f"Failed to post: {response.status_code} - {response.text}")
