import os
import sys
import shutil
import re
from optparse import make_option

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.conf import settings
from django.core.files import File

from thathweb.media.models import MediaFile
from thathweb.models import Tag

class Command(BaseCommand):
    """
    This command will bulk import pictures.  It looks for
    jpe(g), and png files.  When run without any args or options,
    it just imports every picture file in the current directory.

    When applying tags to picture imports, use a quoted string delimited
    by comas. Here is  an example:
        python admin.py -t "Here is a tag, and here is another one"
    """

    help = 'Imports pictures into the database and also creates thumbnails'
    tags = []
    tag_args = ''
    files = []
    file_types = r'(png|jpe?g|mp3|mp4|mov|wav|flac)$'

    args = '<PATH ...>'

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
        )

    def handle(self, *args, **options):
        '''
        These function make sure everything is ready in order to start
        creating picture/tag records in the database and copy the files
        to the appropriate location
        '''
        self.initialize()
        self.set_options(args, options)
        self.set_tags()
        self.set_files()

        for img in self.files:
            # Find our image files
            match = re.search(self.file_types, img)

            if match:
                self.stdout.write(img)

                with open(img, 'rb') as image_file:
                    media_file = MediaFile()
                    media_file.title = os.path.basename(image_file.name)
                    media_file.media_file = File(image_file)
                    media_file.thumbnail = File(image_file)
                    media_file.thumbnail_medium = File(image_file)
                    media_file.created_by_id = 1
                    try:
                        media_file.save()
                        media_file.tags = self.tags
                        media_file.save()

                    except IntegrityError:
                        self.stderr.write("%s already exists" % image_file.name)


    def initialize(self):
        if not os.path.exists(settings.MEDIA_ROOT):
            # try to make it
            try:
                os.mkdir(settings.MEDIA_ROOT)
            except OSError:
                self.stderr.write(
                    'MEDIA_ROOT improperly configured: %s' % settings.MEDIA_ROOT
                )
                sys.exit(1)

        if not os.path.exists(settings.MEDIA_ROOT + '/thumbnails'):
            # try to make it
            try:
                os.mkdir(settings.MEDIA_ROOT + '/thumbnails')
            except OSError:
                self.stderr.write(
                    'Error creating thumbnails directory under %s' % settings.MEDIA_ROOT
                )
                sys.exit(1)

    def set_tags(self):
        if self.tag_args:
            tags = self.tag_args.split(',')

            for tag in tags:
                tag = tag.strip()
                slug = slugify(tag)

                try:
                    cur_tag = Tag.objects.get(slug=slug)
                    self.tags.append(cur_tag)
                except ObjectDoesNotExist:
                    new_tag = Tag()
                    new_tag.title = tag
                    new_tag.save()
                    self.tags.append(new_tag)

    def set_options(self, args, options):
        self.paths = args
        self.recurse = options.get('recurse', False)
        self.tag_args = options.get('tags', '')

    def set_files(self):
        if self.recurse:
            for path in self.paths:
                # returns all files recursively
                if os.path.isfile(path):
                    self.files.append(path)
                else:
                    for dir_level in os.walk(path):
                        directory = dir_level[2]
                        dir_name = dir_level[0]

                        for file in directory:
                            if dir_name[-1] == '/':
                                self.files.append(dir_name + file)
                            else:
                                self.files.append(dir_name + '/' + file)
        else:
            print self.paths
            for path in self.paths:
                if os.path.isfile(path):
                    self.files.append(path)
                else:
                    # returns all files in folder non-recursive
                    for f in os.listdir(path):
                        if os.path.isfile(path + f):
                            self.files.append(path + f)
