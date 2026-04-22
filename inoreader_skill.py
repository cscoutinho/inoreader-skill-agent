import requests
from typing import List, Union

class InoreaderSkill:
    """
    A skill for an AI agent to interact with the Inoreader API.
    Allows saving (starring) and removing (unstarring) items from the library.
    """
    
    BASE_URL = "https://www.inoreader.com/reader/api/0"
    
    def __init__(self, app_id: str, app_key: str, access_token: str):
        """
        Initialize the Inoreader API client.
        
        :param app_id: Your Inoreader App ID
        :param app_key: Your Inoreader App Key
        :param access_token: OAuth 2.0 Access Token for the user
        """
        self.app_id = app_id
        self.app_key = app_key
        self.access_token = access_token
        self.session = requests.Session()
        
        # Set default headers for all requests
        self.session.headers.update({
            "AppId": self.app_id,
            "AppKey": self.app_key,
            "Authorization": f"Bearer {self.access_token}"
        })

    def _edit_tag(self, add_tag: str = None, remove_tag: str = None, item_ids: Union[str, List[str]] = None) -> bool:
        """
        Helper method to add or remove a tag from one or more items.
        """
        url = f"{self.BASE_URL}/edit-tag"
        
        data = {}
        if add_tag:
            data['a'] = add_tag
        if remove_tag:
            data['r'] = remove_tag
            
        if isinstance(item_ids, str):
            data['i'] = item_ids
        elif isinstance(item_ids, list):
            # The API supports multiple 'i' parameters, so we can pass a list of tuples
            # e.g., [('i', 'id1'), ('i', 'id2')] but with requests data dict we can just pass a list
            data['i'] = item_ids
            
        response = self.session.post(url, data=data)
        
        if response.status_code == 200 and response.text.strip() == "OK":
            return True
        else:
            print(f"Failed to edit tag. Status: {response.status_code}, Response: {response.text}")
            return False

    def save_item(self, item_ids: Union[str, List[str]]) -> bool:
        """
        Save items to the library by adding them to the 'Starred' items.
        
        :param item_ids: A single article ID or a list of article IDs.
        :return: True if successful, False otherwise.
        """
        # The system tag for starring/saving an item
        star_tag = "user/-/state/com.google/starred"
        return self._edit_tag(add_tag=star_tag, item_ids=item_ids)

    def remove_item(self, item_ids: Union[str, List[str]]) -> bool:
        """
        Remove items from the library by un-starring them.
        
        :param item_ids: A single article ID or a list of article IDs.
        :return: True if successful, False otherwise.
        """
        star_tag = "user/-/state/com.google/starred"
        return self._edit_tag(remove_tag=star_tag, item_ids=item_ids)

    def add_custom_tag(self, tag_name: str, item_ids: Union[str, List[str]]) -> bool:
        """
        Save items to a custom folder/tag in the library.
        
        :param tag_name: The name of the tag/folder (e.g., 'Read Later')
        :param item_ids: A single article ID or a list of article IDs.
        :return: True if successful, False otherwise.
        """
        custom_tag = f"user/-/label/{tag_name}"
        return self._edit_tag(add_tag=custom_tag, item_ids=item_ids)

# Example usage for the Agent
if __name__ == "__main__":
    # The agent would typically inject these credentials from its environment or secret store
    APP_ID = "YOUR_APP_ID"
    APP_KEY = "YOUR_APP_KEY"
    ACCESS_TOKEN = "YOUR_OAUTH_ACCESS_TOKEN"
    
    agent_skill = InoreaderSkill(app_id=APP_ID, app_key=APP_KEY, access_token=ACCESS_TOKEN)
    
    # Example item ID
    # Note: Shortened IDs are preferred per the Inoreader docs (e.g., "1234567890")
    # Long format also supported (e.g., "tag:google.com,2005:reader/item/1234567890")
    sample_item_id = "1234567890"
    
    # Save the item
    # agent_skill.save_item(sample_item_id)
    
    # Remove the item
    # agent_skill.remove_item(sample_item_id)
