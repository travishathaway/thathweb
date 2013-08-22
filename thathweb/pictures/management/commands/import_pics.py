import os, shutil, re, Image
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from thathweb.pictures.models import Picture

class Command(BaseCommand):
    help = 'Imports pictures into the database and also creates thumbnails'
    thumb_size = (128,128)
    nowstr = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    def handle(self, *args, **options):
        self.initialize()

        imgs = [ settings.UPLOAD_IMG_SRC_DIR+img for img in os.listdir(settings.UPLOAD_IMG_SRC_DIR) ]

        for img in imgs:
            # Find our image files
            match = re.search('(png|jpe?g)$',img)

            if match:
                self.stdout.write(img)

                thumb_dest = settings.UPLOAD_IMG_DEST_DIR + \
                'thumbnails/thmb_'+os.path.basename(img)

                dest = settings.UPLOAD_IMG_DEST_DIR + os.path.basename(img)

                # only create the new files if they don't already exist
                if not os.path.exists(thumb_dest) and not os.path.exists(dest):
                    # copy the original to it's new location
                    shutil.copyfile(img, dest)

                    # create the thumbnail image
                    im = Image.open(img)
                    im.thumbnail(self.thumb_size, Image.ANTIALIAS)
                    im.save(thumb_dest, "JPEG")

                    # make a database record
                    p = Picture()
                    p.title = os.path.basename(img)
                    p.path  = 'uploads/'+os.path.basename(img)
                    p.thumbnail_path = 'uploads/thumbnails/thmb_'+os.path.basename(img)
                    p.save()

                else:
                    self.stderr.write(img+', already exists. Skipping')

    def initialize(self):
        if not os.path.exists(settings.UPLOAD_IMG_DEST_DIR):
            # try to make it
            try:
                os.mkdir(settings.UPLOAD_IMG_DEST_DIR)
            except OSError, e:
                self.stderr.write(e.args)
        if not os.path.exists(settings.UPLOAD_IMG_SRC_DIR):
            # try to make it
            try:
                os.mkdir(settings.UPLOAD_IMG_SRC_DIR)
            except OSError, e:
                self.stderr.write(e.args)
