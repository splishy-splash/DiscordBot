from apscheduler.schedulers.asyncio import AsyncIOScheduler


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.start()
    return scheduler
