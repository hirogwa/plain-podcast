plain-podcast
=============
A plain Django application to host podcast.

## Features
* episode pre-uploading
* RSS feed with iTunes tags

## Installation
* Python dependency
  * `pip install -r requirements.txt`
* Project settings
  * add the plain-podcast app
  * define `STATIC_URL`, `STATIC_ROOT` for css/js/images storage
  * define `MEDIA_URL`, `MEDIA_ROOT` for audio storage
* App settings
  * define `PROJECT_ROOT`, `PRIVATE_FILE_ROOT`, `PRIVATE_FILE_URL` in settings.py
  * create and place css file.  In the applications's root directory,
    1. `mkdir static/podcast -p`
    1. `sass sass/default-style.sass static/podcast/style.css`
* Nginx
  * define locations `/static/`, `/media/`, `/media-private/`, accordingly in the nginx.conf

## License
plain-podcast is released under [MIT license](http://opensource.org/licenses/MIT).
