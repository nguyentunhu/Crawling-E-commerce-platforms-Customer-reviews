from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import pandas as pd
from logger import get_logger
import sys
from utils import setup_driver, save_to_csv

logger = get_logger()
driver = setup_driver()

def extract_comments_from_page(soup):
    comments = []
    
    comment_items = soup.select("div.boxReview-comment-item")
    logger.info(f"Found {len(comment_items)} comment items on page")
    
    for item in comment_items:
        try:
            # Extract username 
            username_elem = item.select_one("div.block-info__name span.name")
            username = username_elem.text.strip() if username_elem else "Anonymous"
            
            # Extract date 
            date_elem = item.select_one("p.date-time")
            date = date_elem.text.strip() if date_elem else ""
            
            # Extract content 
            content_elem = item.select_one("div.comment-content p")
            content = content_elem.text.strip() if content_elem else ""

            comment_data = {
                "username": username,
                "date": date,
                "content": content,
            }
            comments.append(comment_data)
            
        except Exception as e:
            logger.error(f"Error processing a comment: {str(e)}")
    
    return comments

def get_comments(driver, target_count=200, max_clicks=20):
    all_comments = []
    
    base_url = "https://cellphones.com.vn/iphone-15-pro-max/review"
    
    logger.info(f"Navigating to main page: {base_url}")
    driver.get(base_url)
    
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.boxReview-comment-item"))
        )
    except TimeoutException:
        logger.warning("Timed out waiting for initial comments to load")
    
    # Get initial comments
    soup = BeautifulSoup(driver.page_source, "html.parser")
    initial_comments = extract_comments_from_page(soup)
    all_comments.extend(initial_comments)
    logger.info(f"Extracted {len(initial_comments)} initial comments")
    
    click_count = 0
    
    while click_count < max_clicks and len(all_comments) < target_count:
        try:
            button_selectors = [
                "a.has-text-centered.button_view-more-review.is-flex.is-align-items-center.is-justify-content-center.load-more",
                "a.load-more",
                "a.button_view-more-review",
                "a:contains('Xem thêm')"
            ]
            
            load_more_button = None
            for selector in button_selectors:
                try:
                    if not ":contains" in selector:
                        load_more_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    else:
                        text_content = selector.split("'")[1]
                        load_more_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{text_content}')]"))
                        )
                    
                    if load_more_button:
                        logger.info(f"Found 'Xem thêm' button with selector: {selector}")
                        break
                except:
                    continue
            
            if not load_more_button:
                logger.info("No 'Xem thêm' button found. Reached the end of comments.")
                break
                
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_button)
            time.sleep(1)  
            
            driver.execute_script("arguments[0].click();", load_more_button)
            logger.info(f"Clicked 'Xem thêm' button (click #{click_count+1})")
            
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            current_comments = extract_comments_from_page(soup)
            
            if len(current_comments) <= len(all_comments):
                logger.warning("No new comments loaded after clicking. Breaking loop.")
                break
                
            new_comments = current_comments[len(all_comments):]
            all_comments = current_comments 
            
            logger.info(f"Loaded {len(new_comments)} new comments after click #{click_count+1}")
            logger.info(f"Total comments so far: {len(all_comments)}")
            
            click_count += 1
            
        except Exception as e:
            logger.warning(f"Error clicking 'Xem thêm' button: {str(e)}")
            break
    
    logger.info(f"Total comments collected: {len(all_comments)}")
    return all_comments[:target_count]

def crawl_cellphones():
    start_time = time.time()
    driver = setup_driver()
    
    try:
        comments = get_comments(driver, target_count=200, max_clicks=20)
        filename = "data/cellphones.csv"
        save_to_csv(comments, filename)

    except Exception as e:
        logger.error(f"Critical error in crawl_cellphones function: {str(e)}")
    finally:
        driver.quit()
        logger.info(f"Script completed in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    try:
        if sys.stdout.encoding.lower() != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    crawl_cellphones()