import time
from bs4 import BeautifulSoup
import config as cfg
import kkconn
import modules.collect.dir as dir
# from datetime import datetime, timedelta

# def date_range(start, end):
#     start = datetime.strptime(start, "%Y-%m-%d")
#     end = datetime.strptime(end, "%Y-%m-%d")
#     dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
#     return dates


def get_url(work, target_page_no, chromeDriver, conf):
    url_set = set([])

    if int(target_page_no) > 0:
        channel = work["channel"]
        keyword = work["keyword"]
        start_date = work["start_date"]
        end_date = work["end_date"]
        url = cfg.get_collect_url(channel, target_page_no, keyword, start_date, end_date, config_path=dir.config_path)
        chromeDriver.get(url)

        time.sleep(conf[channel]["delay_time"])  # Crome Drive가 소스를 받는데 시간이 필요함
        soup = BeautifulSoup(chromeDriver.page_source, "html.parser")
        try:
            items = soup.find_all('a')
            for item in items:
                url_set.add(item["href"])

        except Exception as e:
            print(e)

    return url_set


def collect_urls(work):

    conf = cfg.get_config(path=dir.config_path)
    chromeDriver = cfg.get_chrome_driver(config_path=dir.config_path)

    current_url_count = 0
    channel = work["channel"]
    limit_url_count = conf[channel]["limit_url_count"]
    target_page_no = 1
    while True:
        try:
            url_list = []
            url_set = get_url(work, target_page_no, chromeDriver, conf)
            for url in list(url_set):
                url_list.append(url)

            if len(url_list) > 0:
                kkconn.kafka_producer(url_list, work)
                current_url_count += len(url_list)
                print("Inserted {} URLS: {}, Current: {}".format(work["channel"], len(url_list), current_url_count))

            if current_url_count > limit_url_count:
                break

            target_page_no += 1

        except Exception as e:
            print(e)

    chromeDriver.close()
# if __name__ == "__main__":
#
#     work_list = [
#         {
#             "channel": "dna",
#             "keyword": "코로나 백신",
#             "start_date": "2021-09-01",
#             "end_date": "2021-09-30",
#             "work_type": "collect_url",
#             "work_group_no": 2,
#         }
#
#     ]
#
#     for work in work_list:
#         date_list = date_range("2021-09-01", "2021-09-30")
#         for date in date_list:
#             work["start_date"] = date
#             work["end_date"] = date
#             collect_urls(work)
