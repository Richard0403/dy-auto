# -*- coding: utf-8 -*-

import asyncio

from apscheduler.schedulers.blocking import BlockingScheduler

from speech_control import SpeechControl


def job_1():
    app = SpeechControl()
    asyncio.run(app.main())

if __name__ == '__main__':
    app = SpeechControl()
    asyncio.run(app.main())

    # scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    # # scheduler.add_job(job_1, 'cron', day='1-31', hour='5', minute='20', misfire_grace_time=180)
    # scheduler.add_job(job_1, "interval",  seconds=30 * 60, id='myfunA')
    # scheduler.start()
