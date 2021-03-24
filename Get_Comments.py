"""module for grabbing comment ID's in the same way that pushshift did using PRAW. 
commentsList returns a list of comment ID's. 
If you are using this make sure you also have an app on Reddit to call with and create a praw.ini
file at the root of your project directory."""

def getSubComments(comment, allComments, verbose = True):
    allComments.append(comment)
    if not hasattr(comment, "replies"):
        replies = comment.comments()
        if verbose: print("fetching (" + str(len(allComments)) + " comments fetched total)")
    else:
        replies = comment.replies
    for child in replies:
        getSubComments(child, allComments, verbose=verbose)


def getAll(r, submissionId, verbose = True):
    submission = r.submission(submissionId)
    comments = submission.comments
    commentsList = []
    for comment in comments:
        getSubComments(comment, commentsList, verbose = verbose)
    return commentsList