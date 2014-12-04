#!/usr/bin/env python

import re
from sqlalchemy.sql import text
from tweetsql.database import Base, db_session, engine
from tweetsql.model import Tweet, User, Word

all_media = []
hashtags = []

REGEX = '#(\w+)'
re_hash = re.compile(r'#[0-9a-zA-Z+_]*',re.IGNORECASE);

for t in db_session.query(Tweet)[0:10]: #.filter(text('tweet ~ :reg')).params(reg=REGEX)[0:10]: 
	all_media.append(t.tweet)
	print t.created_at

# 	for w in t.tweet.split():
# 		hashtag = re_hash.match(w)

# 		if(hashtag):
# 			hashtags.append(hashtag.string)
	
print len(all_media)