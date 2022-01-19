# coding: utf-8

import redshift_connector
import os
from urllib.parse import urlparse

def make_cursor():
	redshift_url = os.environ['DATABASE_URL_REDSHIFT']
	url = urlparse(redshift_url)
	conn = redshift_connector.connect(
	    host=url.hostname,
	    database=url.path.strip('/'),
	    user=url.username,
	    password=url.password
	 )
	cursor: redshift_connector.Cursor = conn.cursor()
	return cursor
