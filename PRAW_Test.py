"""Just a test module to figure out how to use PRAW (Python Reddit API Wrapper)
I still can't figure PRAW out, so I'll come back to this later."""

import praw
import Get_Comments

reddit = praw.Reddit('bot1')

res = Get_Comments.getAll(reddit, "hrp8sb")

for comment in res:
    print(comment.body)