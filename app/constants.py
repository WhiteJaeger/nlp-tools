import pathlib

APP_DIR = pathlib.Path(__file__).parent.parent.resolve()
UPLOADS_DIR = pathlib.Path().joinpath(APP_DIR, 'uploads')
IMAGES_DIR = pathlib.Path().joinpath(APP_DIR, 'images')
