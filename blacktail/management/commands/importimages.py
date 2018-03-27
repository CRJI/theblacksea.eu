import os
import shutil
from pathlib import Path
from willow.image import Image
from django.core.management.base import BaseCommand
from django.db import connection

cursor = connection.cursor()

class WillowImage():

    def __init__(self, path):
        fp = open(path, 'rb')
        img = Image.open(fp)
        dimensions = img.get_size()

        self.width = dimensions[0]
        self.height = dimensions[1]


class Command(BaseCommand):
    help = "Imports all images from a given path into a collection"

    def add_arguments(self, parser):
        parser.add_argument('start_id', type=int)
        parser.add_argument('collection_id', type=int)
        parser.add_argument('images_path', nargs='+', type=str)

        parser.add_argument('-n', '--no-commit', dest='dry', action='store_true')
        parser.set_defaults(no_commit=False)

    def handle(self, *args, **options):
        image_id = options['start_id']
        collection_id = options['collection_id']
        dry = options['dry']

        def copy_image(src, dest):
            destination_path = dest.replace('imported/images/', 'imported/')
            destination_dir = os.path.dirname(destination_path)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            if not dry:
                shutil.copy(src, destination_path)
            return destination_path

        extensions = ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'gif']

        for directory in options['images_path']:
            if os.path.exists('./images'):
                os.unlink('./images')
            os.symlink(directory, './images')
            for extension in extensions:
                pathlist = Path('./images').glob(f'**/*.{extension}')
                for path in pathlist:
                    path_str = str(path)
                    destination_path = copy_image(
                        path_str,
                        os.path.join('./media/original_images/imported/', path)
                    )
                    if not dry:
                        img = WillowImage(destination_path)
                    else:
                        img = WillowImage(path_str)

                    title = (' '.join(path_str.split('/')[1:])).replace(f'.{extension}', '')
                    width = img.width
                    height = img.height
                    file_path = destination_path.replace('./media/', '')
                    file_size = path.stat().st_size

                    sql = """
                        INSERT INTO wagtailimages_image
                        ("id", "title", "file", "width", "height", "created_at", "uploaded_by_user_id", "file_size", "collection_id")
                        VALUES (%s, right(%s, 255), right(%s, 100), %s, %s, NOW(), %s, %s, %s)
                        """

                    print(sql)
                    if not dry:
                        cursor.execute(sql, (image_id, title, file_path, width, height, , 1, file_size, collection_id))
                    else:
                        print(sql % (image_id, title, file_path, width, height, , 1, file_size, collection_id))
                        print(title, width, height, file_path, file_size, '\n')

                    image_id += 1


            os.unlink('./images')
