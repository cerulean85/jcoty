import os
import time

import pandas as pd

import config as cfg
import modules.collect.dir as dir
from modules.zhbase.ZHPandas import ZHPandas

pd.set_option("display.max_rows", None)

conf = cfg.get_config(path=dir.config_path)
csv_save_dir = conf["storage"]["csv_save_dir"] + "/4/nav/"

zhp = ZHPandas()
count = 0
for file in os.listdir(csv_save_dir):
    if not ".csvf" in file:
        txt = zhp.read_csv(csv_save_dir + file)
        print("Dir:", csv_save_dir + file, "Count:", count)
        print(txt[0:50])
        time.sleep(3)
        count += 1

# import url_collector
# from datetime import datetime, timedelta
#
# def date_range(start, end):
#     start = datetime.strptime(start, "%Y-%m-%d")
#     end = datetime.strptime(end, "%Y-%m-%d")
#     dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
#     return dates


# if __name__ == "__main__":


# for

# work_list = [{
#         "channel": "nav",
#         "keyword": "코로나",
#         "start_date": "2021-09-26",
#         "end_date": "2021-09-28",
#         "work_type": "collect_url",
#         "work_group_no": 9,
#         "work_no": 1
#     }]
#
# url_collector.collect_urls(work_list)

# import os
# import pandas as pd
#
# from modules.extractor.TFAnaly import TFAnaly
# from modules.extractor.TFPreProc import TFPreProc
# from modules.extractor.TFWebDoc import TFWebDoc
# from modules.zhbase.ZHPandas import ZHPandas
# from modules.zhbase.ZHPickle import ZHPickle
#
# if __name__ == '__main__':
#
#     # tfp = TFPreProc()
#     # for index in range(1):
#     #     no = index + 1
#     #     tfw = TFWebDoc()
#     #     tfw.test_create_text_blocks("jna", "./jna_test/", "jna_web_doc_{}.html".format(no), "코로나")
#     #
#     #     for tb in tfw.get_tb_arr():
#     #         print(tb.get_parent_tags_pattern())
#     # print(tfw.get_tb_arr())
#     # dom = tfp.create_dom("./jna_test/jna_web_doc_1.html")
#     # print(dom)
#
#     zhpk = ZHPickle()
#     # df = zhpk.load("./modules/eda/dataset/jna_df.pickle")
#     # print(len(df))
#
#     # zhp = ZHPandas()
#     # tfa = TFAnaly()
#     # features_df = zhp.create_data_frame_to_dict(tfa.get_context_feature(df))
#     # zhpk.save("./modules/eda/dataset/jna_merged_DS.pickle", features_df)
#     # print(features_df.head())
#
#     df = zhpk.load("D:/__programming/whateverdot/collector/modules/eda/dataset/jna_merged_3201_DS.pickle")
#     # df[df.x12 == "html/body/div/div/div/div/div/div/div"].y = 0
#     # df[df.x12 == "html/body/div/div/div/div/div/div/div"].y = 0
#     # d = df[(df.x12 == "html/body/div/div/div/div/div/div/div") & (df.y == 1)]
#
#     remove_ptps = [
#         'html/body/div/div/div/div/div/div/a',
#         'html/body/div/div/div/div/div/div/div/div/div/a',
#         'html/body/div/div/div/div/div',
#         'html/body/div/div/div/div/div/div/div/div/h2',
#         'html/body/div/div/div/div/div/div/div/div/p/span',
#         'html/body/div/div/div/div/div/div/div/div/h3',
#         'html/body/div/div/div/div/div/div/div/dl/dd/span/strong'
#         # 'html/body/div/div/div/div/div/div/div'
#     ]
#
#     add_ptps = [
#         'html/body/div/div/div/div/div/div/div/ul/li/a'
#     ]
#
#     for ptp in remove_ptps:
#         df.loc[(df.x12 == ptp), 'y'] = 0
#
#     for ptp in add_ptps:
#         df.loc[(df.x12 == ptp), 'y'] = 1
#
#     print(len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0)]),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 1)]))
#     # exit()
#
#     texts = []
#     ddf = df.loc[((df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0))].x11.tolist()
#
#     candidate_texts = []
#     texts = list(set(ddf))
#     for text in texts:
#         if not ("입력" in text) and not ("수정" in text):
#             candidate_texts.append(text)
#
#     count = 0
#     index_list = df.index[(df.x12 == 'html/body/div/div/div/div/div/div/div')].tolist()
#     for index in index_list:
#         d = df.loc[index, ["x11", "x12", 'y']]
#         df.loc[index, 'y'] = 0 if d.x11 in candidate_texts else 1
#
#         if count % 3000 == 0:
#             print(count, '/', len(index_list),
#                   len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0)]),
#                     len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 1)]))
#
#         count += 1
#
#     print(count, '/', len(index_list),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0)]),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 1)]))
#
#     count = 0
#     index_list = df.index[(df.x12 == 'html/body/div/div/div/div/div/div')].tolist()
#     for index in index_list:
#         d = df.loc[index, ["x11", "x12", 'y']]
#         if len(d.x11) <= 12:
#             df.loc[index, 'y'] = 0
#
#         if count % 3000 == 0:
#             print(count, '/', len(index_list),
#                   len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div') & (df.y == 0)]),
#                     len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div') & (df.y == 1)]))
#
#         count += 1
#
#     print(count, '/', len(index_list),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div') & (df.y == 0)]),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div') & (df.y == 1)]))
#     zhpk.save("D:/__programming/whateverdot/collector/modules/eda/dataset/jna_merged_3201_DS.pickle", df)
#
#
#     # for text in candidate_texts:
#     #     df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.x11 == text), 'y'] = 1
#
#     # print(len(df.query("x11 in " + str(candidate_texts))))
#     # print(df.y == 1)
#     # df.query("x11 in " + str(candidate_texts)).y = 1
#     # print(df.query("x11 in " + str(candidate_texts)).y)
#     # print(df.query("x11 in " + str(candidate_texts)))
#     # print(df.loc[df.x11 in candidate_texts])
#     # df.loc[df.query("x11 in " + str(candidate_texts)), 'y'] = 1
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/a')].head())
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/div/div/div/a')].head())
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div')].head())
#     # print(df.loc[((df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0)), ["x11", "y"]])
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/div/div/h2')].head())
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/div/div/p/span')].head())
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/div/div/h3')].head())
#
#     # print(df[df.freq_rank])
#     #
#     # df = None
#     # zhp = ZHPandas()
#     # path = "D:/__programming/__data2/jna/label/"
#     # for file in os.listdir(path):
#     #     if ".csv" in file:
#     #         if df is None:
#     #             df = pd.read_csv(path + file)
#     #         else:
#     #             df = zhp.concat_row(df, pd.read_csv(path + file))
#     #
#     #         print(len(df))
