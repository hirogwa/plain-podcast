"""
Set up script for plainpodcast
"""
import os
import subprocess

SASS_DIR = os.path.join(os.path.dirname(__file__), 'sass')
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static', 'plainpodcast')


def compilesass(s):
    """
    Compiles one sass file to css
    :param s: name of the sass file
    """
    print('compiling {}.sass...'.format(s))

    origin = os.path.join(SASS_DIR, s, '{}.sass'.format(s))
    dest = os.path.join(STATIC_DIR, s, '{}.css'.format(s))
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    subprocess.call(['sass', origin, dest])

    return True


def setup():
    # sass to css
    list(map(compilesass, os.listdir(SASS_DIR)))


if __name__ == "__main__":
    setup()
