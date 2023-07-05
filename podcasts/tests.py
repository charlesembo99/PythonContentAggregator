from django.test import TestCase
from .models import Episode
from django.utils import timezone
# Create your tests here.
class PodcastsTestCase(TestCase):
    
    def setUp(self):
        self.episode = Episode.objects.create(
            title='This is a test title',
            description='This is a test description',
            episode_url='https://myawesomeshow.com',
            thumbnail= 'https://image.myawesomeshow.com',
            postcast_name='This is a test post cast',
            guide = 'de194720-7b4c-49e2-a05f-432436d3fetr'
        )
    
    def test_podcast_model(self):
        self.assertEqual(self.episode.title,'This is a test title')
        self.assertEqual(self.episode.description,'This is a test description')
        self.assertEqual(self.episode.episode_url,'https://myawesomeshow.com')
        self.assertEqual(self.episode.postcast_name,'This is a test post cast')
        self.assertEqual(self.episode.guide,'de194720-7b4c-49e2-a05f-432436d3fetr')

    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')
        self.assertContains(response,'Homepage')
