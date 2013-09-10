import os, shutil, re, Image
from optparse import make_option
from pprint import pprint
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from thathweb.pictures.models import Picture, PictureTag

class Command(BaseCommand):
    """
    This command will bulk import pictures.  It looks for 
    jpe(g), and png files.  When run without any args or options,
    it just imports every picture file in the current directory.

    When applying tags to picture imports use a quoted string delimited
    by comas. Here is  an example:
        python admin.py -t "Here is a tag, and here is another one"
    """

    help = 'Imports pictures into the database and also creates thumbnails'
    thumb_size = (128,128)
    tags = []
    tag_args = ''
    files = []
    webroot_path = 'uploads/'

    option_list = BaseCommand.option_list + (
        make_option('-t', '--tags',
            action='store',
            type='string',
            nargs=1,
            dest='tags',
            default='',
            help='Tags to apply to pictures'),
        make_option('-r', '--recurse',
            action='store_true',
            dest='recurse',
            default=False,
            help='Recurse in to directories when looking for pictures'),
        make_option('-f', '--folder',
            action='store',
            type='string',
            nargs=1,
            dest='folder',
            default='./',
            help='Folder to scan for pictures. Defaults to current directory'),
        )

    def handle(self, *args, **options):
        # These function make sure everything is ready in order to start
        # creating picture/tag records in the database and copy the files
        # to the appropriate location
        self.initialize()
        self.set_options(options)
        self.set_tags()
        self.set_files()

        for img in self.files:
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
                    p.path  = self.webroot_path+os.path.basename(img)
                    p.thumbnail_path = self.webroot_path+'thumbnails/thmb_'+os.path.basename(img)
                    
                    p.save()

                    # add tags 
                    for tag in self.tags:
                        p.picture_tag.add(tag)

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

        if not os.path.exists(settings.UPLOAD_IMG_DEST_DIR+'/thumbnails'):
            # try to make it
            try:
                os.mkdir(settings.UPLOAD_IMG_DEST_DIR+'/thumbnails')
            except OSError, e:
                self.stderr.write(e.args)

    def set_tags(self):
        if self.tag_args != '':
            tags = self.tag_args.split(',')
            for tag in tags:
                tag = tag.strip()
                slug = slugify(tag)

                try:
                    cur_tag = PictureTag.objects.get(name=slug)
                    self.tags.append(cur_tag)

                except ObjectDoesNotExist:
                    new_tag = PictureTag()
                    new_tag.name = slug
                    new_tag.title = tag
                    new_tag.save()
                    self.tags.append(new_tag)

    def set_options(self, options):
        if os.path.exists(options.get('folder')):
            self.folder  = options['folder']
        else:
            raise Exception(options['folder']+" does not exist.")

        self.recurse = options.get('recurse', False)
        self.tag_args = options.get('tags', '')

    def set_files(self):
        if self.recurse:
            # returns all files recursively
            for dir_level in os.walk(self.folder):
                directory = dir_level[2]
                dir_name  = dir_level[0]

                for file in directory:
                    if dir_name[-1] == '/':
                        self.files.append(dir_name+file)
                    else:
                        self.files.append(dir_name+'/'+file)
        else:
            # returns all files in folder non-recursive
            self.files = [ file for file in os.listdir(self.folder) if os.path.isfile(file)]
