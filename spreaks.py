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
        self.shows = self.__get_shows()

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

    def __get_shows(self):
        """Get a list of show_id from the user
        TODO: by default only 50 elements given. Check 'next_url' item in the json file
        """
        r = requests.get(
            f'https://api.spreaker.com/v2/users/{self.user_id}/shows')
        items = r.json().get('response').get('items')
        shows = [items[i].get('show_id') for i in range(len(items))]
        return shows

    # def __get_favorites(self):
    #     """Get a list of favorite shows of the user
    #     Requires authentication and ownership...
    #     TODO: by default only 50 elements given. Check 'next_url' item in the json file
    #     TODO: show favorites requires owner authentication. Delete method?
    #     """
    #     OAUTH_TOKEN = os.environ['BEEP_SPREAKS_TOKEN']
    #     headers = {'Authorization': f'Bearer {OAUTH_TOKEN}', }
    #     r = requests.get(
    #         f'https://api.spreaker.com/v2/users/{self.user_id}/favorites?limit=3', headers=headers)
    #     items = r.json().get('response').get('items')
    #     shows = [items[i].get('show_id') for i in range(len(items))]
    #     return shows

    def contact(self):
        """Returns all available user contact information
        """
        contact_sources = ['contact_email', 'website_url',
                           'facebook_permalink', 'twitter_username']
        contact = {key: getattr(self, key, "") for key in contact_sources
                   if getattr(self, key) is not None}
        return contact


class Show:
    """Show class to hold all the information of a show retrieved from the API
    """

    def __init__(self, target) -> None:
        """Creates a new Show instance by retrieveing info from the API
        Arguments:
        - target: either the 'show_id' or the 'permalink` of the show
        """
        show_info = self.__get_data(target=target)
        # Explicit assignment for easier understanding
        self.show_id = show_info.get('show_id')
        self.title = show_info.get('title')
        self.image_url = show_info.get('image_url')
        self.image_original_url = show_info.get('image_original_url')
        self.explicit = show_info.get('explicit')
        self.author_id = show_info.get('author_id')
        self.last_episode_at = show_info.get('last_episode_at')
        self.site_url = show_info.get('site_url')
        self.description = show_info.get('description')
        self.category_id = show_info.get('category_id')
        self.language = show_info.get('language')
        self.permalink = show_info.get('permalink')
        self.cover_image_url = show_info.get('cover_image_url')
        self.cover_offset = show_info.get('cover_offset')
        self.episodes_sorting = show_info.get('episodes_sorting')
        # Skip 'author', since we already have the 'author_id'
        self.website_url = show_info.get('website_url')
        self.email = show_info.get('email')
        self.facebook_url = show_info.get('facebook_url')
        self.itunes_url = show_info.get('itunes_url')
        self.twitter_name = show_info.get('twitter_name')
        self.skype_name = show_info.get('skype_name')
        self.tel_number = show_info.get('tel_number')
        self.sms_number = show_info.get('sms_number')

    def __repr__(self) -> str:
        return f"{self.title} ({self.permalink} - {self.show_id}):\n{self.description}"

    def __get_data(self, target=None):
        """Get public show data
        """
        if target is None:
            target = self.show_id
        r = requests.get(f'https://api.spreaker.com/v2/shows/{target}')
        response = r.json().get('response')
        if r.status_code == 200:
            show_info = response.get('show')
            return show_info
        else:
            raise Exception('Code {code}: {messages}'.format(**r.get('error')))
