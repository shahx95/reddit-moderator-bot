from replit import db
from functions import *
import os, requests, random, praw, time, traceback, re
from datetime import datetime, date
# from alive import alive

existing_db_keys = db.keys() #{'whitelist', 'blacklist', 'filteredSubs', 'mods'}
default_values = {
    'whitelist': [], #You can populate this list with any existing list of whitelisted users you may have
    'blacklist': [], #You can populate this list with any existing list of blacklisted users you may have
    'filteredSubs': [], #Enter the names of subreddits that promote community interference in your subreddit  
    'mods': []  # Enter the usernames of mods
}

#initialize replit db
for key in default_values:
    if key not in existing_db_keys:
        db[key] = default_values[key]



reddit = praw.Reddit(client_id=os.getenv('client_id'),
                     client_secret=os.getenv('client_secret'),
                     password=os.getenv('password'),
                     user_agent=os.getenv('user_agent'),
                     username=os.getenv('username'))

#keep the bot alive on Replit
# alive()

#static information
mod_sub = os.getenv('mod_sub')
subreddit = reddit.subreddit(os.getenv('mod_sub'))

#streaming of comments and submissions
submission_stream = reddit.subreddit(mod_sub).stream.submissions(
  pause_after=-1, skip_existing=True)

comment_stream = reddit.subreddit(mod_sub).stream.comments(pause_after=-1,
                                                           skip_existing=True)


#bot starting
line = "*" * 30
print(line)
print("Starting moderation")
print(line)


while True:
  time.sleep(30) #precaution to ensure compliance with rate limitations
  
  try:
    #start streaming post submissions
    for submission in submission_stream:

      print("Checking submissions\n")
      
      if submission is None:
        break
    
      current_author = submission.author.name
      #brigading precaution function
      is_brigading_result = is_brigading(current_author)
  
      if is_brigading_result:
          submission.mod.lock()
          submission.mod.remove()
          print('Removed submission from', current_author)

      #cool down function
      cooldown(current_author, submission)

        

    
    #start streaming comments
    for comment in comment_stream:
      
      print("Checking comments\n")
      
      if comment is None:
        break
      
      whitelist_command(comment)  
      
      current_author = comment.author.name
      is_brigading_result = is_brigading(current_author)
      print(current_author, is_brigading_result)
  
      if is_brigading_result:
          comment.mod.lock()
          comment.mod.remove()
          print('Removed comment from', current_author)

  except Exception:
    #fallback to handle any unexpected or unhandled exceptions that occur within the preceding try block
    print(traceback.format_exc())
