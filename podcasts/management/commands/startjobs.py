#django imports
from django.conf import settings
from django.core.management.base import BaseCommand
#standard library
import logging
#models
from  podcasts.models import Episode
#third party 
import feedparser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from dateutil import parser
logger = logging.getLogger(__name__)

def save_episode_feed(feed):
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image['href']
    for item in feed.entries:
        if not Episode.objects.filter(guide=item.guid).exists():
            episode = Episode(
                    title = item.title,
                    description = item.description,
                    episode_url=item.link,
                    thumbnail=podcast_image,
                    postcast_name = podcast_title,
                    guide = item.guid
            )
            episode.save()


def fetch_real_python():
    _feed=feedparser.parse('https://realpython.com/podcasts/rpp/feed');
    save_episode_feed(_feed)


def fetch_talkpython_episodes():
    _feed=feedparser.parse('https://talkpython.fm/episodes/rss')
    save_episode_feed(_feed)

def delete_old_job_executions(max_age=604800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    def handle(self,*args, **options):
        scheduler=BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(),"default")
        
        scheduler.add_job(
            fetch_real_python,
            trigger='interval',
            minutes=2,
            id="The Real Python Podcast",
            max_instances=1,
            replace_existing=True
        )
        logger.info(
            'Added job : The Real Python Podcast.'
        )
        scheduler.add_job(
            fetch_talkpython_episodes,
            trigger='interval',
            minutes=2,
            id="Talk Python Feed",
            max_instances=1,
            replace_existing=True
        )
        logger.info(
            'Added job : Talk Python Feed'
        )
        scheduler.add_job(
            delete_old_job_executions,
            trigger = CronTrigger(
                day_of_week='mon',hour='00',minute='00'
            ),
            id='Delete Old Job Executions',
            max_instances=1,
            replace_existing=True
        )
        try:
            logger.info('starting scheduler ....')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('stopping the schedular ..')
            scheduler.shutdown()
            logger.info('scheduler shutdown succesfully ..')


        
        
        
       