#!/usr/bin/env python

import json
import twitter
from tweetsql.database import Base, db_session, engine
from tweetsql.model import Tweet, User, Word, Hashtag
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

OAUTH_TOKEN = '-'
OAUTH_TOKEN_SECRET = ''

twitter_auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = twitter.TwitterStream(auth=twitter_auth)

statuses = twitter_stream.statuses.filter(track='Temple Mount, Palestine')

for t in statuses:
    # print(t['text'])
    try:
        u = db_session.query(User).filter_by(uid=str(t['user']['id'])).one()
    except MultipleResultsFound:
        u = User(screen_name=t['user']['screen_name'], uid=t['user']['id'])
        pass
    except NoResultFound:
        u = User(screen_name=t['user']['screen_name'], uid=t['user']['id'])
        db_session.add(u)
        db_session.commit()

    if t['coordinates']:
        tw = Tweet(tweet=t['text'], tid=t['id'], user_id=u.id, created_at=t['created_at'], coordinates=t['coordinates']['coordinates'])
    else:
        tw = Tweet(tweet=t['text'], tid=t['id'], user_id=u.id, created_at=t['created_at'])

    try:
        words = tw.tweet.split()
        for w in words:
            try:
                w_obj = db_session.query(Word).filter(Word.word == w).one()
            except MultipleResultsFound:
                pass
            except NoResultFound:
                w_obj = Word(word=w)
                db_session.add(w_obj)
                db_session.commit()
                tw.words.append(w_obj)
        db_session.add(tw)
        db_session.commit()
    except OperationalError:
        db_session.rollback()

    if (t['entities']['hashtags']):
        for h in t['entities']['hashtags']:
            try:
                ht = Hashtag(hashtag=h['text']) 
                print u.uid
                print tw.tid
                ht.users.append(u)
                ht.tweets.append(tw)        
                db_session.add(ht)
                db_session.commit()                
            except OperationalError:
                db_sesson.rollback()