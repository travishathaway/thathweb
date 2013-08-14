import os, re, Image
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports pictures into the database and also creates thumbnails'
    thumb_size = (128,128)
    nowstr = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    def handle(self, *args, **options):
        try:
            imgs = os.listdir(settings.IMG_IMPORT_DIR)
            imgs = [ settings.IMG_IMPORT_DIR+img for img in imgs ]
        except OSError, e:
            self.stderr.write(e)
            return

        for img in imgs:
            # Find our image files
            match = re.search('(png|jpe?g)$',img)

            if match:
                self.stdout.write(img)

                # Create the thumbnail
                if not os.path.exists( 
                    settings.STATIC_ROOT+ \
                    '/img/uploads/thumbnails/'+self.nowstr
                ):

                    os.mkdir( settings.STATIC_ROOT + \
                    '/img/uploads/thumbnails/'+self.nowstr)

                thumb_dest = settings.STATIC_ROOT + \
                    '/img/uploads/thumbnails/'+self.nowstr+'/thmb_'+ \
                    os.path.basename(img)
                im = Image.open(img)
                im.thumbnail(self.thumb_size, Image.ANTIALIAS)
                im.save(thumb_dest, "JPEG")
