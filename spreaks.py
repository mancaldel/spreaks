import os
import json
import requests


class User:
    """User class to hold all the information of a user retrieved from the API
    """

    def __init__(self, target) -> None:
        """Create a new user by retrieveing info from the API
        Arguments:
        - target: either the 'user_id' or the 'username` of the user
        """
        user_info = self.__get_data(target=target)
        # Explicit assignment for easier understanding
        self.user_id = user_info.get('user_id')
        self.fullname = user_info.get('fullname')
        self.site_url = user_info.get('site_url')
        self.image_url = user_info.get('image_url')
        self.image_original_url = user_info.get('image_original_url')
        self.accept_latest_tos_url = user_info.get('accept_latest_tos_url')
        self.username = user_info.get('username')
        self.description = user_info.get('description')
        self.kind = user_info.get('kind')
        self.plan = user_info.get('plan')
        self.followers_count = user_info.get('followers_count')
        self.followers_ids = self.__get_followers()
        self.followings_count = user_info.get('followings_count')
        self.followings_ids = self.__get_followings()
        self.shows_count = user_info.get('shows_count')
        self.contact_email = user_info.get('contact_email')
        self.website_url = user_info.get('website_url')
        self.facebook_permalink = user_info.get('facebook_permalink')
        self.twitter_username = user_info.get('twitter_username')

    def __repr__(self) -> str:
        return f"{self.fullname} ({self.username} - {self.user_id}): {self.description}"

    def __get_data(self, target=None):
        """Get public user data
        """
        if target is None:
            target = self.user_id
        r = requests.get(f'https://api.spreaker.com/v2/users/{target}')
        response = r.json().get('response')
        if r.status_code == 200:
            user_info = response.get('user')
            return user_info
        else:
            raise Exception('Code {code}: {messages}'.format(**r.get('error')))

    # def __get_my_data(self):
    #     """Return private data of a user using their OAUTH-TOKEN
    #     This returns a lot of new user variables
    #     Requires Authentication
    #     TODO: should I implement this?
    #     """
    #     OAUTH_TOKEN = os.environ['BEEP_SPREAKS_TOKEN']
    #     headers = {'Authorization': f'Bearer {OAUTH_TOKEN}', }
    #     response = requests.get('https://api.spreaker.com/v2/me', headers=headers)

    def __get_followers(self):
        """Get user_id of the follower
        TODO: by default only 50 elements given. Check 'next_url' item in the json file
        """
        r = requests.get(
            f'https://api.spreaker.com/v2/users/{self.user_id}/followers')
        items = r.json().get('response').get('items')
        followers_ids = [items[i].get('user_id') for i in range(len(items))]
        return followers_ids

    def __get_followings(self):
        """Get user_id of followed users
        TODO: by default only 50 elements given. Check 'next_url' item in the json file
        """
        r = requests.get(
            f'https://api.spreaker.com/v2/users/{self.user_id}/followings')
        items = r.json().get('response').get('items')
        following_ids = [items[i].get('user_id') for i in range(len(items))]
        return following_ids

    # def __get_blocked(self):
    #     """Get list of blocked users
    #     This returns a lot of other variables
    #     Requires Authentication
    #     TODO: should I implement this?
    #     TODO: by default only 50 elements given. Check 'next_url' item in the json file
    #     """
    #     OAUTH_TOKEN = os.environ['BEEP_SPREAKS_TOKEN']
    #     headers = {'Authorization': f'Bearer {OAUTH_TOKEN}', }
    #     r = requests.get(
    #         f'https://api.spreaker.com/v2/users/{self.user_id}/blocks', headers=headers)
    #     items = r.json().get('response').get('items')
    #     blocked_ids = [items[i].get('user_id') for i in range(len(items))]
    #     return blocked_ids

    def contact(self):
        """Returns all available user contact information
        """
        contact_sources = ['contact_email', 'website_url',
                           'facebook_permalink', 'twitter_username']
        contact = {key: getattr(self, key, "") for key in contact_sources
                   if getattr(self, key) is not None}
        return contact
