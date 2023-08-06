import json
from stockly_python_common.query import Query
from stockly_python_common.stockly_utils import _common

class StocklyClient:
    """stockly client"""

    def __init__(self, api_key: str, auth_url: str, api_url: str) ->None:
        self.api_key = api_key
        self.auth_url = auth_url
        self.api_url = api_url
    
    def get_bot_user_permission_list(self,list_type:str,stockly_userid:int,bot_id:str)->dict:
        """_summary_

        Args:
            list_type (str): watchlist/alert/portfolio
            stockly_userid (int): stockly userid
            bot_id (str): stockly bot id

        Returns:
            _type_: if particular user give bot permission then this api return list of that user
        """
        query=Query.get_bot_user_permission_list(list_type=list_type,stockly_userid=stockly_userid,bot_id=bot_id,apikey=self.api_key)
        return _common(url=self.api_url,key="getBotUserPermissionList",query=query,return_type={})

    def add_bot_user_specific_configs(self,stockly_user_id:int,bot_id:str,config:dict)->dict:
        """_summary_

        Args:
            stockly_user_id (int): stockly userid
            bot_id (str): bot id i.e XX@.stockly.network
            config (dict): {"A":200,"B":500}

        Raises:
            Exception: config must be in dict format

        Returns:
            dict: return response dict
        """
        if isinstance(config,dict):
            config=json.dumps(config)
            query=Query.add_bot_user_specific_configs(stockly_user_id=stockly_user_id,bot_id=bot_id,data=config,apikey=self.api_key)
            return _common(url=self.api_url, key="addBotUserSpecificConfigs",query=query,res=True,return_type={})
        raise Exception("Config type must be python dict")
    
    
           
    def get_bot_user_specific_configs(self,bot_id:str,stockly_user_id:int=None):
        """_summary_

        Args:
            bot_id (str): bot id i.e XX@.stockly.network
            stockly_user_id (int, optional): _description_. Defaults to None.

        Returns:
            _type_: return dict of your config 
        """
        query=Query.get_bot_user_specific_configs(stockly_user_id=stockly_user_id,bot_id=bot_id,apikey=self.api_key)
        return _common(url=self.api_url, key="getBotUserSpecificConfigs",query=query,return_type={})

    def get_bot_subscribe_user_developer(self,bot_id:str)->list:
        """_summary_

        Args:
            bot_id (str): _description_

        Returns:
            list: _description_
        """
        query=Query.get_bot_subscribe_user_developer(bot_id=bot_id,apikey=self.api_key)
        return _common(url=self.api_url, key="getBotSubscribeUserDeveloper",query=query,return_type=[])