plain-podcast
=============
A plain Django application to host podcast.

## Features
* episode pre-uploading

## Installation

* Project settings
  * add the plain-podcast app
  * define `STATIC_URL`, `STATIC_ROOT` for css/js/images storage
  * define `MEDIA_URL`, `MEDIA_ROOT` for audio storage
* App settings
  * define `PROJECT_ROOT`, `PRIVATE_FILE_ROOT`, `PRIVATE_FILE_URL` in settings.py
* Nginx
  * define locations `/static/`, `/media/`, `/media-private/`, accordingly in the nginx.conf
