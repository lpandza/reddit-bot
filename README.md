# reddit-bot

## Setup Instructions

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Reddit credentials**
   - Open `config.ini`
   - Use the default credentials or replace with your own Reddit account information:
     ```ini
     [credentials]
     client_id = YOUR_CLIENT_ID
     client_secret = YOUR_CLIENT_SECRET
     username = YOUR_REDDIT_USERNAME
     password = YOUR_REDDIT_PASSWORD
     ```
   - Save the file
4. **Run the script**
   ```bash
   python main.py
   ```
## Notes
- To obtain API credentials, visit: https://www.reddit.com/prefs/apps and create a new app
- Select "script" as the application type
