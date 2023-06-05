#insert utility functions in this file
#primary utility functions are already added 

from replit import db
import praw, os

reddit = praw.Reddit(client_id=os.getenv('client_id'),
                     client_secret=os.getenv('client_secret'),
                     password=os.getenv('password'),
                     user_agent=os.getenv('user_agent'),
                     username=os.getenv('username'))


#filter submissions by users who have a potential history of trolling or spreading hate against your subreddit
def background_check(author):
    banned_word_array = ['word_example1', 'word_example2']  # Insert troll/hate words in this list

    # Check user post history
    for submission in reddit.redditor(author).submissions.new(limit=None):
        # Check for user using hateful words
        for word in banned_word_array:
            if word in str(submission.title).lower() or word in str(submission.selftext).lower():
                return True
        # Check for user participating in suspect subreddits
        if submission.subreddit.display_name in db['filteredSubs']:
            return True

    # Check user comment history
    for comment in reddit.redditor(author).comments.new(limit=None):
        for word in banned_word_array:
            if word in str(comment.body).lower():
                return True

        if comment.subreddit.display_name in db['filteredSubs']:
            return True

    return False

#check user status in the subreddit i.e. whitelisted, blacklisted or requires a background check
def is_brigading(author):
    if author in db['whitelist']:
        return False
    elif author in db['blacklist']:
        print("Blacklisted")
        return True
    else:
        return background_check(author)

#remove submissions if user exceeds daily limit for posting
def cooldown(author, new_submission):
  new_submission_time = new_submission.created_utc
  daily_limit = 5 #daily limit is at 5 posts currently
  total = 0

  for submission in reddit.redditor(author).submissions.new(limit=None):

    if submission.subreddit == os.getenv('mod_sub'):
      if submission.is_robot_indexable:
        total = total + 1
        submission_time = submission.created_utc
    if total > daily_limit:
      check_time = new_submission_time - submission_time
      if check_time < 86400:
        print("Cooling down user: " + author)
        message = f'''Hi. 

It seems like you are trying to post more than {daily_limit} times in the last 24 hours. We want to give everyone a chance to post and be seen, so we limit everyone to {daily_limit} posts per 24 hours. 

If you think this post has been wrongly removed, you can [reach out to the mods](https://www.reddit.com/message/compose?to=/r/{os.getenv('mod_sub')}).

___

^(This comment has been posted automatically.)'''
        new_submission.mod.remove()
        new_submission.reply(message).mod.distinguish(sticky=True)


#mod comment command to whitelist a user on the go
def whitelist_command(comment):
    if comment.body == "!whitelist" and comment.author.name in db['mods']:
        # If mod comment is made directly on a post
        if comment.parent_id[1] == "3":
            post_identity = comment.parent_id[3:]
            post = reddit.submission(id=post_identity)
            
            if post.locked:
                post.mod.unlock()
            
            post.mod.approve()
            
            create_note = f"Whitelisted by {comment.author.name}"
            post.mod.create_note(label=None, note=create_note)
            
            # Add author to whitelist array
            print(f"{comment.author.name} has whitelisted {post.author.name}")
            temp = db['whitelist']
            temp.append(comment.author.name)
            db['whitelist'] = temp

        # If mod comment is made as a reply to a comment
        if comment.parent_id[1] == "1":
            comment_identity = comment.parent_id[3:]
            comment_object = reddit.comment(id=comment_identity)
            
            if comment_object.locked:
                comment_object.mod.unlock()
            comment_object.mod.approve()
            
            create_note = f"Whitelisted by {comment.author.name}"
            comment_object.mod.create_note(label=None, note=create_note)
            
            # Add author to whitelist array
            print(f"{comment.author.name} has whitelisted {comment_object.author.name}")
            temp = db['whitelist']
            temp.append(comment.author.name)
            db['whitelist'] = temp

        # Remove mod comment command
        comment.mod.remove()
        if comment.author.name == os.getenv('username'):
            comment.delete()
