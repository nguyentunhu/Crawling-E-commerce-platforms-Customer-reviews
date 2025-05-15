from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd 
from logger import get_logger

logger = get_logger()

edge_options = Options()
edge_options.add_argument("--headless")  
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--disable-dev-shm-usage")
edge_options.add_argument("--window-size=1920,1080")
edge_options.add_argument("--ignore-ssl-errors=yes")
edge_options.add_argument("--ignore-certificate-errors")
edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/134.0.3124.72")
    
def setup_driver():
    try:
        webdriver_path = EdgeChromiumDriverManager().install()
        logger.info(f"Using WebDriver from: {webdriver_path}")
        service = Service(webdriver_path)
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        logger.error(f"Error setting up WebDriver: {str(e)}")
        return None
    
def save_to_csv(comments, filename):
    if not comments:
        logger.warning("No comments to save")
        return
    
    df = pd.DataFrame(comments)
    df.to_csv(filename, index=False, encoding="utf-8-sig") 
    logger.info(f"Saved {len(comments)} comments to {filename}")