import os
import time

import config as cfg
import modules.collect.dir as dir

from modules.extractor.ExtractorTextNode import ExtractorTextNode
from modules.zhbase.ZHPickle import ZHPickle


def create_doc_text_blocks(work):

    channel = work["channel"]
    target_path = work["target_file_path"]
    file_name = work["file_name"]
    keyword = work["keyword"]
    date = work["date"]
    save_file_path = work["save_file_path"]

    content_ptp_list = work["model"]["content_ptp_list_path"]
    taf_rank_dict = work["model"]["taf_rank_path"]
    taf_boundary_rank = work["model"]["taf_boundary_rank"]

    try:
        mid_text_nodes = 'text,ptp,taf_rank\n'
        str_text_nodes = 'text,keyword,date,channel\n'
        wd = ExtractorTextNode()
        items = wd.create_text_node_list(target_path + '/', file_name)
        for item in items:
            text = item["text"]
            ptp = item["ptp"]
            taf_rank = 1 if taf_rank_dict.get(text) is None else taf_rank_dict.get(text)
            mid_text_nodes += '{},{},{}\n'.format(text, ptp, taf_rank)
            if (ptp in content_ptp_list) and (taf_rank <= taf_boundary_rank):
                str_text_nodes += '{},{},{},{}\n'.format(text,keyword,date,channel)
        print(str_text_nodes)

        with open(save_file_path, "w", encoding="utf-8") as f:
            f.write(str_text_nodes)
        with open(save_file_path + 'f', "w", encoding="utf-8") as f:
            f.write(mid_text_nodes)

        print("Converted [{}]...".format(save_file_path))
    except Exception as e:
        print(e)


def work():
    conf = cfg.get_config(path=dir.config_path)
    html_save_dir = conf["storage"]["html_save_dir"]
    csv_save_dir = conf["storage"]["csv_save_dir"]
    model_path = dir.model_path
    channel_spec = conf["channel_spec"]

    models = {}
    zhpk = ZHPickle()
    for channel in channel_spec:
        if models.get(channel) is None:
            if conf["model"].get(channel) is not None:
                content_ptp_list_path = dir.model_path + channel + '/' + conf["model"][channel]["content_ptp_list"]
                taf_rank_path = dir.model_path + channel + '/' + conf["model"][channel]["taf_rank"]
                taf_boundary_rank = conf["model"][channel]["taf_boundary_rank"]

                models[channel] = {
                    "content_ptp_list_path": zhpk.load(content_ptp_list_path),
                    "taf_rank_path": zhpk.load(taf_rank_path),
                    "taf_boundary_rank": taf_boundary_rank
                }

    last_index_check = {}
    d = []
    while True:
        for html_save_group_dir, _, _ in os.walk(html_save_dir):
            if html_save_dir == html_save_group_dir:
                continue

            for html_save_channel_path, _, _ in os.walk(html_save_group_dir):
                if html_save_group_dir == html_save_channel_path:
                    continue

                if len(os.listdir(html_save_channel_path)) > 0:
                    if last_index_check.get(html_save_channel_path) is None:
                        last_index_check[html_save_channel_path] = 0

                file_list = os.listdir(html_save_channel_path)
                file_list.sort(key=lambda x: (len(x), x))

                for file in file_list:
                    tmp = file.split('.')
                    tmp = tmp[0].split('_')
                    channel = tmp[0]
                    work_group_no = tmp[1]
                    keyword = tmp[2]
                    date = tmp[3]
                    index = int(tmp[len(tmp)-1])
                    if last_index_check[html_save_channel_path] < index:
                        last_index_check[html_save_channel_path] = index
                        d.append(index)
                        work = {
                            "channel": channel,
                            "work_group_no": work_group_no,
                            "keyword": keyword,
                            "date": date,
                            "index": index,
                            "target_file_path": html_save_channel_path,
                            "file_name": file,
                            "model": models[channel],
                            "save_file_path": cfg.get_save_dir(csv_save_dir, work_group_no, channel) +
                                              cfg.get_save_filename(channel, work_group_no, keyword, date, index, "csv")
                        }

                        create_doc_text_blocks(work)
                        # print(d)

        time.sleep(5)
        # print(file.split(.))


# file_path = conf["storage"]["save_dir"] + channel
# os.listdir(file_path)


work()
