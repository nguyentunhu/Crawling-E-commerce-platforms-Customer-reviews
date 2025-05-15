from selenium.webdriver.edge.options import Options
from thegioididong_crawler import crawl_tgdd
from cellphones_crawler import crawl_cellphones
# from fpt_crawler import crawl_fpt
from tinhte_crawler import crawl_tinhte
from logger import get_logger
from bot_detector import detect_bots
import pandas as pd
from utils import save_to_csv

logger = get_logger()


if __name__ == "__main__":
    logger.info("Starting comment crawling process.")
    try:
        crawl_tgdd()
        crawl_cellphones()  # only 50 comments available (5 cmts/ page x 10 pages in total)
        crawl_tinhte()
        # crawl_fpt()

        tgdd = pd.read_csv("data/tgdd.csv")
        tgdd["source"] = "thegioididong.com"

        cellphones = pd.read_csv("data/cellphones.csv")
        cellphones["source"] = "cellphones.vn"

        tinhte = pd.read_csv("data/tinhte.csv")
        tinhte["source"] = "tinhte.vn"

        main_df = pd.concat([tgdd, cellphones, tinhte])
        logger.info("Successfully merge datasets.")

        detect_bots(main_df)
        logger.info("Successfully detect bot-generated comments.")
        
        logger.info("Crawling process completed.")

    except Exception as e:
        print(e)
