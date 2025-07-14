import pandas as pd

def parse_channel_mappings(excel_file_path):
    df = pd.read_excel(excel_file_path, sheet_name='Channelssubreddit')
    
    mappings = {}
    
    for _, row in df.iterrows():
        channel = row['Heartbeat Channel Name']
        subreddits = []
        for col in ['Srape from Subreddit 1', 'Srape from Subreddit 2', 'Srape from Subreddit 3']:
            sub = row.get(col)
            if pd.notna(sub):
                subreddits.append(sub.strip())
        if subreddits:
            mappings[channel] = subreddits
    
    return mappings

if __name__ == "__main__":
    # Make sure the file is in the same directory as this script
    excel_path = 'AI Community SOP.xlsx'
    channel_map = parse_channel_mappings(excel_path)
    for channel, subs in channel_map.items():
        print(f"Channel: {channel} -> Subreddits: {subs}")
