from typing import Tuple, List

import patreon
from dotenv import load_dotenv
from os import getenv


class Patreon:
    def __init__(self):
        self.access_token = getenv("ACCESS_TOKEN")
        self.api_client = patreon.API(self.access_token)
        self.campaign_response = self.api_client.fetch_campaign()
        self.campaign_id = self.campaign_response.data()[0].id()


def verified_patron_email(email: str) -> Tuple[bool, str]:
    load_dotenv()
    all_pledges = gather_all_patrons()
    return find_patron_email(all_pledges, email)


def find_patron_email(all_pledges: list, email: str) -> Tuple[bool, str]:
    for pledge in all_pledges:
        declined = pledge.attribute('declined_since')
        reward_tier = pledge.relationships()['reward']['data']
        pledge_email = pledge.relationship('patron').attribute('email')

        if pledge_email == email:
            reward_tier = pledge.relationship('reward').attribute('amount_cents') if reward_tier else 0
            if not declined and reward_tier >= 500:
                return True, "Successfully found active Patron"
            return False, "Successfully found Patron, but subscription is not active"
    return False, "Could not find Patron with provided email. Please check your Patreon account information"


def gather_all_patrons() -> List:
    all_pledges = []
    cursor = None
    patreon_setup = Patreon()
    api_client = patreon_setup.api_client

    while True:
        pledges_response = api_client.fetch_page_of_pledges(
            campaign_id=patreon_setup.campaign_id,
            page_size=25,
            cursor=cursor,
            fields={'pledge': 'declined_since'}
        )
        cursor = api_client.extract_cursor(pledges_response)
        all_pledges += pledges_response.data()
        if not cursor:
            break
    return all_pledges
