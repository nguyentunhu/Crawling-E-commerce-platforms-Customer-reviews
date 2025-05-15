import pandas as pd
import re
from logger import get_logger

logger = get_logger()

def detect_bots(comments:pd.DataFrame):
    try:
        ## Repeated content
        comments["bot_patterns"] = comments["content"].duplicated(keep=False).map({True: "Repeated content"})
        logger.info(f"Identify {len(comments[comments['bot_patterns'] == 'Repeated content'])} repeated contents.")

        # Spam URLs
        comments.loc[comments["content"].str.contains(r"http?://\S+", regex=True, na=False), "bot_patterns"] = "Contain URLs"
        logger.info(f"Identify {len(comments[comments['bot_patterns'] == 'Contain URLs'])} comments containing URLs.")
        # Generic usernames
        comments.loc[comments["content"].str.contains(r"username?://\S+", regex=True, na=False), "bot_patterns"] = "Generic username"
        logger.info(f"Identify {len(comments[comments['bot_patterns'] == 'Generic username'])} comments by generic usernames.")

        # Mark bot-generated comments
        comments["bot_generated"] = comments["bot_patterns"].notna().astype(int)

        comments.to_csv("data/bot-detected_data.csv")
    except Exception as e:
        print(e)

