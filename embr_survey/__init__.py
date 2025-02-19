# get this stuff out of the way so that when we create the window,
# we don't end up with programmable/fixed-function conflict
import os
import sys
import logging
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

# remove HTML tags from strings


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


is_exe = getattr(sys, 'frozen', False)
# https://stackoverflow.com/a/39215961/2690232


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.DEBUG):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


def setup_logger(pth, now):
    embr_logger = logging.getLogger('embr_survey')
    embr_logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(os.path.join(pth, '%slog.log' % now))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sl = StreamToLogger(embr_logger, logging.DEBUG)
    if is_exe:
        sys.stderr = sl
    embr_logger.addHandler(fh)

    gatt_logger = logging.getLogger('pygatt')
    gatt_logger.setLevel(logging.DEBUG)
    gatt_logger.addHandler(fh)


# https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
if is_exe:
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = os.path.join(sys.executable, '..')  # sys.executable for onefile option
else:
    application_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
