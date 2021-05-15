# -*- coding: utf-8 -*- #
from datetime import datetime

AUTHOR = 'Vimal A.R'
SITENAME = 'arvimal.github.io'
SITEURL = 'https://arvimal.github.io'

BROWSER_COLOR = "#333333"
PYGMENTS_STYLE = "monokai"

ROBOTS = "index, follow"

THEME = "octopress"
DISPLAY_TAGS_ON_SIDEBAR_LIMIT = 10
PATH = 'content'

TIMEZONE = 'Europe/Amsterdam'
I18N_TEMPLATES_LANG = "en"
DEFAULT_LANG = "en"
OG_LOCALE = "en_US"
LOCALE = "en_US"

DATE_FORMATS = {
    "en": "%B %d, %Y",
}

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
USE_FOLDER_AS_CATEGORY = False
MAIN_MENU = True
HOME_HIDE_TAGS = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'https://getpelican.com/'),

# Social widget
SOCIAL = (
    ("github", "https://github.com/arvimal"),
    ("rss", "/blog/feeds/all.atom.xml"),
)

MENUITEMS = (
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)

CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa",
}

COPYRIGHT_YEAR = datetime.now().year
DEFAULT_PAGINATION = 10

#DISQUS_SITENAME = "flex-pelican"
#ADD_THIS_ID = "ra-55adbb025d4f7e55"

#STATIC_PATHS = ["images", "extra/ads.txt", "extra/CNAME"]

#EXTRA_PATH_METADATA = {
#    "extra/ads.txt": {"path": "ads.txt"},
#    "extra/CNAME": {"path": "CNAME"},
#}
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

USE_LESS = True

# GOOGLE ANALYTICS
# For Google Analytics 4 use. Note that for old Google Analytics ('UA-XXXXX') the GOOGLE_ANALYTICS variable is included in publishconfig.py
# GOOGLE_GLOBAL_SITE_TAG = 'G-XXXXX'
