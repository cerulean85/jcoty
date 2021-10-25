import time
from multiprocessing import Process, freeze_support
from datetime import datetime, timedelta
import dbconn
import url_collector_nav as ucnb
import url_collector_twt as uct
import url_collector_ins as uci
import url_collector_dna as ucd

def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    return dates

def collect_urls(work):

    channel = work["channel"]
    general_type = ["nav", "twt", "dna", "jna"]
    if channel in general_type:
        date_list = date_range(work["start_date"], work["end_date"])
        for date in date_list:
            work["start_date"] = date
            work["end_date"] = date

            if channel == "nav":
                ucnb.collect_urls(work)

            if channel == "twt":
                uct.collect_urls(work)

            if channel == "dna":
                ucd.collect_urls(work)

    if channel == "ins":
        uci.collect_urls(work)


if __name__ == '__main__':
    freeze_support()

    while True:
        # DB 조회
        work_group_list = dbconn.session.query(dbconn.WorkGroups).filter(
            dbconn.WorkGroups.work_state == 'attached').all()
        for wg in work_group_list:
            dbconn.session.query(dbconn.WorkGroups) \
                .filter(dbconn.WorkGroups.id == wg.id) \
                .update({dbconn.WorkGroups.work_state: "working"})
            dbconn.session.commit()

            channels = wg.channels.split(',')
            procs = []
            for channel in channels:
                keywords = wg.keywords.split(',')
                for keyword in keywords:
                    work = {
                        "channel": channel,
                        "keyword": keyword,
                        "start_date": str(wg.start_date),
                        "end_date": str(wg.end_date),
                        "work_type": "collect_url",
                        "work_group_no": wg.id,
                    }
                    procs.append(Process(target=collect_urls, args=(work,)))

            for proc in procs:
                proc.start()

        time.sleep(3)
        # dbconn.session.commit()

    # time.sleep(120)