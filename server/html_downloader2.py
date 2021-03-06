from datetime import datetime
import json
import os
from multiprocessing import Process

from selenium.webdriver.common.keys import Keys

import config as cfg
import kkconn
import modules.collect.dir as dir
import time
import pandas as pd
from collections import Counter
import sys

from kafka import TopicPartition

conf = cfg.get_config(path=dir.config_path)
consumer = kkconn.kafka_consumer("urls")
html_save_dir = conf["storage"]["html_save_dir"]
csv_save_dir = conf["storage"]["csv_save_dir"]
channel_spec = conf["channel_spec"]


def work(work_channel_type):
    chromeDriver = cfg.get_chrome_driver(dir.config_path)
    pre_total = 0
    curr_val = 0
    accum_val = 0
    while True:
        # print("Waiting...")
        # time.sleep(60)

        # partitions = []
        # for partition in consumer.partitions_for_topic("urls"):
        #     partitions.append(TopicPartition("urls", partition))
        #
        # partitions = consumer.end_offsets(partitions)
        # offset_val = 0
        #
        # for key, val in partitions.items():
        #     offset_val += val
        #
        # curr_val = offset_val - pre_total
        # if pre_total != 0:
        #     accum_val += curr_val
        #
        # print(datetime.now().strftime('%H:%M:%S.%f')[:-3], "|", offset_val, "|", curr_val, "|", accum_val)
        # pre_total = offset_val

        # consumer.seek("urls", 0)
        # consumer.commit()
        records = consumer.poll(3000)
        for tp, record in records.items():

            ins_login = False
            url_counter_dict = {}
            for item in record:
                url_info = json.loads(str(item.value.decode('utf-8')))

                channel = url_info["channel"]
                if work_channel_type != channel:
                    continue

                work_group_no = url_info["work_group_no"]
                date = url_info["date"]
                keyword = url_info["keyword"].replace("'", "")

                if channel == "ins" and not ins_login:
                    ins_login = True
                    cfg.ins_login(chromeDriver, dir.config_path)

                if url_counter_dict.get(channel) is None:
                    url_counter_dict[channel] = {
                        "counter": Counter(),
                        "work_group_no": work_group_no,
                        "keyword": keyword,
                        "date": date
                    }

                url_counter_dict[channel]["counter"].update(url_info["urls"])

            for channel, value in url_counter_dict.items():
                work_group_no = value["work_group_no"]
                keyword = value["keyword"]
                date = value["date"]
                dup_limit_count = conf[channel]["duplicated_limit_count"]

                cfg.make_dir(html_save_dir, work_group_no, channel_spec)
                cfg.make_dir(csv_save_dir, work_group_no, channel_spec)

                for url_count in value["counter"].items():
                    url = url_count[0]
                    dup_count = url_count[1]

                    if dup_count > dup_limit_count:
                        print("Dup File Info: {}, {}, {}, {}, {}".
                              format(url, dup_count, work_group_no, keyword, date))
                        continue

                    switch_to_iframe = conf[channel]["switch_to_iframe"]
                    try:
                        chromeDriver.get(url)
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        print("Can't collect {}".format(url))
                        continue

                    if switch_to_iframe:
                        try:
                            iframe = chromeDriver.find_element_by_tag_name('iframe')
                            chromeDriver.switch_to.frame(iframe)
                            time.sleep(1)
                        except Exception as e:
                            print(e)
                            continue

                    filepath = cfg.get_save_dir(html_save_dir, work_group_no, channel)
                    index = len(os.listdir(filepath))
                    filename = cfg.get_save_filename(channel, work_group_no, keyword, date, index + 1, "html")
                    save_file_path = filepath + filename

                    with open(save_file_path, "w", encoding="utf-8") as f:
                        f.write(str(chromeDriver.page_source))

                    time.sleep(3)
        #             print('Written {}...'.format(save_file_path))


if __name__ == "__main__":
    procs = []
    procs.append(Process(target=work, args=("nav",)))
    for proc in procs:
        proc.start()
    # for record in records:
    #     print(record.value)
    # url_info = json.loads(str(message.value.decode('utf-8')))
    # url_counter.update(url_info["urls"])
    # for item in url_counter.items():
    #     print(item[0], item[1], count)
    # channels = []
    # for message in consumer:
    #     url_info = json.loads(str(message.value.decode('utf-8')))
    #     url_counter.update(url_info["urls"])
    #     for item in url_counter.items():
    #         print(item[0], item[1], count)

    # channels.append(url_info["channel"])
    # print(url_info)
    # url_info = zhp.create_data_frame_to_dict(url_info)
    # print(url_info, count)
    # print( url_info["channel"] + str(count))
    # print(count)
    # print(len(channels))
    # channel = ""
    # work_group_no, work_no = 0, 0
    # url_objs = []
    #
    # conf = cfg.get_config(path=dir.config_path)
    # file_path = conf["storage"]["save_dir"] + channel
    # switch_to_iframe = conf[channel]["switch_to_iframe"]
    # index = 0
    # chromeDriver = cfg.get_chrome_driver(dir.config_path)
    #
    # for item in url_objs:
    #     url = item["url"]
    #     chromeDriver.get(url)
    #
    #     if switch_to_iframe:
    #         try:
    #             iframe = chromeDriver.find_element_by_tag_name('iframe')
    #             chromeDriver.switch_to.frame(iframe)
    #             time.sleep(1)
    #         except Exception as e:
    #             print(e)
    #             continue
    #
    #     file_info = {
    #         "channel": channel,
    #         "source": chromeDriver.page_source,
    #         "filepath": file_path,
    #         "filename": channel + "_web_doc_" + str(work_group_no) + '_' + str(work_no) + '_' + str(index + 1)
    #     }
    #
    #     with open(file_info["filepath"] + '/' + file_info["filename"], "w", encoding="utf-8") as f:
    #         f.write(str(file_info["source"]) + ".html")
    #     print('Written {}...'.format(file_info["filename"]))
    #
    #     time.sleep(conf[channel]["delay_time"])
    #     index += 1
    #
    # chromeDriver.quit()
