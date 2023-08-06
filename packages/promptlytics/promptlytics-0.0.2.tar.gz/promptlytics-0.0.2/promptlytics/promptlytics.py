import requests

class Promptlytics(object):
    """Instances of Promptlytics are used to track and use templates.

    Args:
        apikey (string): your promptlytics api key
        baseurl (string, optional): override the default api url
    """
    
    def __init__(self, apikey, baseurl="https://www.promptlytics.co" ):
        self.apikey = apikey
        self._endpoints = {
            'track': "{}/api/track".format(baseurl),
            'templates': "{}/api/templates".format(baseurl)
        }

    def track(self, rating, use_selected = False, alias=None, template_text=None, completion=None, input_vars=None):
        """Track a template and rating. If the template doesn't exist, it will be created.

        Args:
            rating (int): rating of the output from your template.
            use_selected (bool, optional): if True, the template selected for use in the dashboard will be used. Defaults to False.
            alias (string, optional): name of your new or existing template. Defaults to None.
            template_text (string, optional): your template. Defaults to None.
            completion (string, optional): text output from the model you are using. Defaults to None.
            input_vars (string[], optional): array of variable names. Defaults to None.
        """

        headers = {
            'api_key': self.apikey 
        }

        if(use_selected):
            payload = {
                "selected": True,
                "completion": completion,
                "rating": rating
            }
        
        else:
            payload = {
                "alias": alias,
                "template_text": template_text,
                "input_vars": input_vars,
                "completion": completion,
                "rating": rating
            }

        response = requests.post(url=self._endpoints["track"], headers=headers, json=payload)

        print(response.json())

    def useTemplate(self, alias = None, use_selected = False):
        """Retrieve a template by its alias or the template selected in your promptlytics dashboard.

        Args:
            alias (string, optional): alias of the template you wish to retrieve. Defaults to None.
            use_selected (bool, optional): if True, the template selected in your promptlytics dashboard will be retrieved. Defaults to False.

        Returns:
            string: the specified template in text format.
        """

        headers = {
                'api_key': self.apikey 
            }
        
        if(use_selected):

            params = {"selected": True}

            response = requests.get(url=self._endpoints["templates"], headers=headers, params=params)
            return response.json()['template_text']


        else:

            response = requests.get(url = self._endpoints["templates"] + "/{}".format(alias), headers=headers)
            print(response.json())
            return response.json()['template_text']
