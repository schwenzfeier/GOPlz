# GOPlz - a Twitter bot to fight the AHCA

### Want to start your own bot?
Create a twitter account, go to [apps.twitter.com](https://apps.twitter.com) to create an app and generate access tokens.

Clone this repo and replace the app secrets with your own:

```
CONSUMER_KEY = os.environ['GOPLZ_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['GOPLZ_CONSUMER_SECRET']
ACCESS_KEY = os.environ['GOPLZ_ACCESS_KEY']
ACCESS_SECRET = os.environ['GOPLZ_ACCESS_SECRET']
```
Then just run the `goplz.py` file. In Mac Terminal it looks like this:
```python goplz.py```

Voila!
