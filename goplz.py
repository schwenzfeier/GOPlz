import speedtest, tweepy, os, time, sys, random
import pandas as pd

CONSUMER_KEY = os.environ['GOPLZ_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['GOPLZ_CONSUMER_SECRET']
ACCESS_KEY = os.environ['GOPLZ_ACCESS_KEY']
ACCESS_SECRET = os.environ['GOPLZ_ACCESS_SECRET']


# 0 - handle 
# 1 - district/state  
# 2 - total_loss 
# 3 - loss_children 
# 4 - disabled_loss
# 5 - elderly_loss

messages = [
'. @{0}, under the #ACHA, your constituents in {1} are at risk. {2} stand to lose health coverage under the new bill. Vote no!',
'Hey @{0}, did you know that under the #ACHA {2} people in {1} will lose health care? #SaveOurCare', 
'. @{0}: Protect American kids! Vote against the #ACHA or {3} kids are going to lose healthcare in {1}!',
'. @{0} - Protect healthcare for {2} of your most vulnerable constituents. Stop the #ACHA! #SaveOurCare',
'. @{0} support the {4} disabled and {5} elderly Medicaid patients in {1}: Stop the #ACHA. #SaveOurCare',
'Hey @{0}, why do you think {3} kids in {1} should lose their healthcare? Stop the #AHCA. #SaveOurCare',
'{2} people in {1} are going to lose their healthcare, @{0} can you tell them why? #SaveOurCare'
]


def PickRepresentative(data_frame, party):
	df = data_frame.loc[(data_frame.party == party)]
	df.index = range(1, len(df) + 1)
	rep_num = random.randrange(1,len(df))
	rep = df.ix[rep_num]

	# making sure we have data for this rep
	if rep['party'] == party and not pd.isnull(rep['total_loss']):
		handle = rep['twitter_handle']
		if pd.isnull(rep['district']):
			district = rep['state']
		else:
			district = rep['state'] + '-' + str(int(rep['district']))
		total_loss = int(rep['total_loss'])
		children_loss = int(rep['medicaid_children'])
		disabled_loss = int(rep['medicaid_disabled'])
		elderly_loss = int(rep['medicaid_elderly'])

		return [handle, district, "{:,}".format(total_loss), "{:,}".format(children_loss), "{:,}".format(disabled_loss), "{:,}".format(elderly_loss)]
	
	else:
		return None

def Resist(rep_info):
	tweet_text = random.choice(messages)
	tweet_text = tweet_text.format(*rep_info)

	# Make sure we stay under 140 characters
	if len(tweet_text) <= 140:
		return tweet_text
	
	else:
		return None


def TweetAThing(text):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	# api.update_status(text)
	print(text)


def GOPlz():
	congress_df = pd.read_csv('data/cong_data_full_merged.csv')
	rep = PickRepresentative(congress_df, party = 'Republican')
	if rep:
		tweet = Resist(rep)
		if tweet:
			TweetAThing(tweet)

if __name__ == '__main__':
	while True:
		GOPlz()
		min_sleep = random.randrange(1,7)
		time.sleep(60*min_sleep)





