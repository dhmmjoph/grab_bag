print "importing..."
import praw, os
r = praw.Reddit("legos_bot by /u/dhmmjoph")
print "logging in..."
r.login(os.environ["reddit_username"], os.environ["reddit_password"])
terms = ["legos", "legoes"]
def banned(comment):
	if comment.user == "legos_bot":
		return True
	if  comment.user in str(r.get_wiki_page("legos_bot", "noreplyusers")):
		print "banned user"
		return True
	if comment.subreddit in str(r.get_wiki_page("legos_bot", "noreplysubs")):
		print "banned sub"
		return True
	return False
def keywords(comment):
	for term in terms:
		if term in comment.body.lower():
			return True
	return False
def reply(comment):
	body = ("Hello %s!  I noticed you used the word /"Lego/" as a plural noun in your comment."
	"While this is a common thing to do, I'd like to take a moment to cordially remind you that"
	"it's considered inaccurate.  For best accuracy, 'LEGO' should be used as an adjective."
	"Instead of 'legos', consider 'LEGO bricks', 'LEGO plates', 'LEGO beams', etc. or just"
	"'bricks', 'plates', or 'beams'.  Thanks!\n---\n"
	"I am a bot, and this reply was sent automatically.  If you'd like to stop recieving replies from me."
	"create a selfpost in /r/legos_bot with the title 'REMOVE'"
	"in the Subject line.  If you'd like me to "
while True:
    subreddit = r.get_subreddit('legos_bot')
    all_comments = subreddit.get_comments()
    for comment in all_comments:
    	if keywords(comment) and not banned(comment):
    		reply(