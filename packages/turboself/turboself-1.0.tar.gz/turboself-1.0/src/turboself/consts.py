'''
Constants module.
'''

import re as regex

class re:
    '''
    Regexes used by the core module.
    '''
    
    # Get the payload in the home page
    get_home_data = regex.compile(r'name=\"(.*?)\".*value=\"(.*?)\"').findall
    
    # Get credits data (credits left, meal representation, unit price)
    get_credits = regex.compile(r'[>\n ]*?(\d+,\d+)|>Soit : (\d*) repas').findall
    
    # Parse user data keys
    get_user_key = regex.compile(r'ctl00_cntForm_UC_HeaderTop_lbl(.*)_Smartphone').findall

# EOF