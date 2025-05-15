from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import sys
import os
from logger import get_logger
from utils import setup_driver, save_to_csv

logger = get_logger()
driver = setup_driver()

def extract_comments_from_page(driver):
    comments = [] 
    comment_boxes = driver.find_elements(By.CSS_SELECTOR, "div[class*='thread-comment__box'], div[id^='post-']")
    logger.info(f"Found {len(comment_boxes)} on current page")
    
    for box in comment_boxes:
        try:
            # Extract username 
            username = "Unknown"
            try:
                username_container = box.find_element(By.CSS_SELECTOR, "div[class*='comment__author-container']")
                username_elem = username_container.find_element(By.CSS_SELECTOR, "a")
                username = username_elem.text.strip()
            except:
                pass
            
            # Extract timestamp
            timestamp = "Unknown"
            try:
                time_elem = box.find_element(By.CSS_SELECTOR, "a[class*='comment_date'], span[title]")
                timestamp = time_elem.text.strip() if time_elem.text else time_elem.get_attribute("title")
            except:
                pass
            
            # Extract content
            content = "No content"
            try:
                content_container = box.find_element(By.CSS_SELECTOR, "div[class*='comment__content']")
                paragraphs = content_container.find_elements(By.CSS_SELECTOR, "span[class*='paragraph'], p")
                if paragraphs:
                    content = "\n".join([p.text.strip() for p in paragraphs])
                else:
                    content = content_container.text.strip()
            except:
                pass
            
            if content != 'No content':
                comment_data = {
                    "username": username,
                    "date": timestamp,
                    "content": content,
                }
                comments.append(comment_data)
                
        except Exception as e:
            logger.error(f"Error in extracting process: {str(e)}")
        
    logger.info(f"Extracted {len(comments)} comments from current page")
    return comments

def get_comments(driver, target_count=200, max_pages=20):
    all_comments = []
    base_url = "https://tinhte.vn/thread/review-iphone-15-pro-max-1tb-van-la-smartphone-dinh-nhat-nhung-khong-con-nhieu-dieu-vui-ve.3769610/"
    range(1,max_pages+1)
    for page in range(1, max_pages): 
        if page == 1:
            url = base_url
        else:
            url = base_url + "page-" + str(page)
        logger.info(f"Navigating to main page: {url}")
        try:
            driver.get(url)
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='thread-comment']"))
                )
            except TimeoutException:
                logger.warning("Timed out waiting for initial comments to load")
            
            time.sleep(3)
            
            initial_comments = extract_comments_from_page(driver)
            all_comments.extend(initial_comments)
            logger.info(f"Extracted {len(initial_comments)} comments from page {page}")
        
        except Exception as e:
            logger.error(f"Error during main scraping process: {str(e)}")

        logger.info(f"Total comments collected: {len(all_comments)}")
        
        if len(all_comments) >= target_count:
            return all_comments
    return all_comments 

def crawl_tinhte():
    start_time = time.time()
    logger.info("----------------BEGIN CRAWLING FROM tinhte.vn")
    driver = setup_driver()
    
    if not driver:
        logger.error("Failed to set up WebDriver. Exiting.")
        return
    
    try:
        comments = get_comments(driver)
        
        os.makedirs("data", exist_ok=True)
        csv_filename = "data/tinhte.csv"
        save_to_csv(comments, csv_filename)
        
    except Exception as e:
        logger.error(f"Critical error in crawl_tinhte function: {str(e)}")
    finally:
        driver.quit()
        logger.info(f"CRAWLING FROM tinhte.vn COMPLETED IN {time.time() - start_time:.2f} SECONDS----------------\n")

if __name__ == "__main__":
    try:
        if sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    
    crawl_tinhte()