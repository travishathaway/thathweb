import requests
import sys

from django.core.files import File
from django.core.urlresolvers import reverse

from thathweb.tests import OepTest
from models import MediaFile


class MediaTestCase(OepTest):
    jpg_url = 'https://upload.wikimedia.org/wikipedia/commons/4/4c/Franz_ferdinand.jpg'
    png_url = 'https://upload.wikimedia.org/wikipedia/en/b/bc/Wiki.png'

    def setUp(self):
        '''
        We create a file that we can use for our test during set up.
        We need a real image file to test our thumbnail generator, so
        we fetch one from the web.
        '''
        super(MediaTestCase, self).setUp()

        with open('/tmp/test.jpg', 'wb') as jpg:
            req = requests.get(self.jpg_url)
            if req.status_code == 200:
                jpg.write(req.content)
            else:
                print('Test jpg not found. Please update your tests.')
                sys.exit(1)

            self.jpg_file = File(jpg)

        with open('/tmp/test.png', 'wb') as png:
            req = requests.get(self.png_url)
            if req.status_code == 200:
                png.write(req.content)
            else:
                print('Test png not found. Please update your tests.')
                sys.exit(1)

            self.png_file = File(png)

        with open('/tmp/test.pdf', 'wb') as pdf:
            pdf.write('''
                Hehehe, it's not really a pdf, but it shouldn't matter.
            ''')
            self.pdf_file = File(pdf)

        with open('/tmp/test.mp4', 'wb') as mp4:
            mp4.write('''
                Again, not really a mp4, but it shouldn't matter.
            ''')
            self.mp4_file = File(mp4)

    def test_upload_jpg(self):
        '''
        Assertions
        - The record was created
        - The file has a thumbnail attribute
        - We can download the file
        '''
        self.login_ed_coordinator()
        self.jpg_file.open('rb')

        self.client.post(
            reverse('thathweb.media.views.media_add_ajax'),
            {
                'title': 'Test jpg',
                'caption': 'This is a test image',
                'files[]': [self.jpg_file, ],
            }
        )

        media_file = MediaFile.objects.get(title='Test jpg')

        self.assertIsNotNone(
            media_file.media_file,
            msg='media_file attribute not set on record'
        )
        self.assertIsNotNone(
            media_file.thumbnail,
            msg='thumbnail attribute not set on record'
        )

    def test_upload_png(self):
        '''
        Assertions
        - The record was created
        - The file has a thumbnail attribute
        - We can download the file
        '''
        self.login_ed_coordinator()
        self.png_file.open('rb')

        self.client.post(
            reverse('thathweb.media.views.media_add_ajax'),
            {
                'title': 'Test png',
                'caption': 'This is a test image',
                'files[]': [self.png_file, ],
            }
        )

        media_file = MediaFile.objects.get(title='Test png')

        self.assertIsNotNone(
            media_file.media_file,
            msg='media_file attribute not set on record'
        )
        self.assertIsNotNone(
            media_file.thumbnail,
            msg='thumbnail attribute not set on record'
        )

    def test_upload_pdf(self):
        '''
        Assertions
        - The record was created
        - We can download the file
        '''
        self.login_ed_coordinator()
        self.pdf_file.open('rb')

        self.client.post(
            reverse('thathweb.media.views.media_add_ajax'),
            {
                'title': 'Test pdf',
                'caption': 'This is a test image',
                'files[]': [self.pdf_file, ],
            }
        )

        media_file = MediaFile.objects.get(title='Test pdf')

        self.assertIsNotNone(
            media_file.media_file,
            msg='media_file attribute not set on record'
        )

    def test_upload_mp4(self):
        '''
        Assertions
        - The record was created
        - We can download the file
        '''
        self.login_ed_coordinator()
        self.mp4_file.open('rb')

        self.client.post(
            reverse('thathweb.media.views.media_add_ajax'),
            {
                'title': 'Test mp4',
                'caption': 'This is a test image',
                'files[]': [self.mp4_file, ],
            }
        )

        media_file = MediaFile.objects.get(title='Test mp4')

        self.assertIsNotNone(
            media_file.media_file,
            msg='media_file attribute not set on record'
        )
