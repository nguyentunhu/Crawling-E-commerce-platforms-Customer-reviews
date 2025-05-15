from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import re
from logger import get_logger
import sys
from utils import setup_driver, save_to_csv

logger = get_logger()
driver = setup_driver()

def extract_date_from_support_text(text):
    date_patterns = [
        r"ngày\s+(\d{1,2}/\d{1,2}/\d{4})",  # ngày DD/MM/YYYY
        r"(\d{1,2}/\d{1,2}/\d{4})"          # DD/MM/YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None

def extract_comments_from_page(soup):
    comments = []
    
    comment_items = soup.select("ul.comment-list > li") or \
                    soup.select("[class*='comment'][class*='item']") or \
                    soup.select("li[id^='r-']")
    
    logger.info(f"Found {len(comment_items)} comment items on page")
    
    for item in comment_items:
        try:
            # Extract username
            username = "Anonymous"
            username_selectors = [".cmt-name", ".name", "[class*='name']", "div.cmt-top strong", "div.cmt-top"]
            for selector in username_selectors:
                user_elem = item.select_one(selector)
                if user_elem and user_elem.text.strip():
                    username = user_elem.text.strip()
                    break
            
            # Extract content
            content = ""
            content_selectors = [
                "p.cmt-txt", 
                ".cmt-content p", 
                ".content", 
                "[class*='content'] p", 
                "div.cmt-content"
            ]
            for selector in content_selectors:
                content_elem = item.select_one(selector)
                if content_elem and content_elem.text.strip():
                    content = content_elem.text.strip()
                    break

            # Extract date 
            date = ""
            support_elem = item.select_one("div.support")
            if support_elem:
                support_text = support_elem.text.strip()
                extracted_date = extract_date_from_support_text(support_text)
                if extracted_date:
                    date = extracted_date
            
            if not date:
                date_selectors = [".time", ".date", "[class*='time']", "[class*='date']", "span.txt-time"]
                for selector in date_selectors:
                    date_elem = item.select_one(selector)
                    if date_elem and date_elem.text.strip():
                        date_text = date_elem.text.strip()
                        extracted_date = extract_date_from_support_text(date_text)
                        if extracted_date:
                            date = extracted_date
                            break
            
            comment_data = {
                "username": username,
                "content": content,
                "date": date
            }
            comments.append(comment_data)
                
        except Exception as e:
            logger.error(f"Error processing a comment: {str(e)}")
    
    return comments

def get_comments(driver, target_count=200, max_pages=20):
    all_comments = []
    
    base_url = "https://www.thegioididong.com/dtdd/iphone-15-pro-max/danh-gia"
    
    for page in range(1, max_pages + 1):
        if len(all_comments) >= target_count:
            logger.info(f"Reached target count of {target_count} comments. Stopping.")
            break
            
        url = base_url if page == 1 else f"{base_url}?page={page}"
        logger.info(f"Navigating to page {page}: {url}")
        
        try:
            driver.get(url)
            
            try:
                WebDriverWait(driver, 15).until(  
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.comment-list > li, [class*='comment'][class*='item'], li[id^='r-']"))
                )
            except TimeoutException:
                logger.warning(f"Timed out waiting for comments on page {page}")
                if "không tìm thấy" in driver.page_source.lower() or "captcha" in driver.page_source.lower():
                    logger.warning("Error page or captcha detected. Stopping pagination.")
                    break
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            page_comments = extract_comments_from_page(soup)
            logger.info(f"Extracted {len(page_comments)} comments from page {page}")
            
            if not page_comments:
                logger.info(f"No comments found on page {page}, likely reached the end")
                break
            
            all_comments.extend(page_comments)
                        
            pagination_exists = False
            pagination_elements = soup.select(".pagination li, .pagcomment a, ul.listpage li, a.btn_showcmt")
            
            if pagination_elements:
                logger.info(f"Found {len(pagination_elements)} pagination elements")
                pagination_exists = True
            else:
                logger.info("No pagination elements found on the page")
                
                load_more = soup.select_one("a.viewmore, button.viewmore, [class*='load-more'], .btn-load-more")
                if load_more:
                    logger.info("Found 'Load more' button")
                    pagination_exists = True
            
            if not pagination_exists and page > 1:
                logger.info("No pagination controls found, stopping")
                break
                
            time.sleep(3)
            
        except Exception as e:
            logger.error(f"Error processing page {page}: {str(e)}")
            
    logger.info(f"Total comments collected: {len(all_comments)}")
    return all_comments[:target_count]
    
def crawl_tgdd():
    start_time = time.time()
    driver = setup_driver()
    
    try:
        logger.info("----------------BEGIN CRAWLING FROM thegioididong.vn")
        comments = get_comments(driver, target_count=200, max_pages=20)
    
        filename = "data/tgdd.csv"
        save_to_csv(comments, filename)
    except Exception as e:
        logger.error(f"Critical error in main function: {str(e)}")
    finally:
        driver.quit()
        logger.info(f"CRAWLING FROM thegioididong.vn COMPLETED IN {time.time() - start_time:.2f} SECONDS----------------\n")

if __name__ == "__main__":
    try:
        if sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    
    crawl_tgdd()