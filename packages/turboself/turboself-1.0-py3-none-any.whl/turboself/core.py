'''
Core module.
'''

import requests
from datetime import datetime
from bs4 import BeautifulSoup as Soup

from typing import Generator
from dataclasses import dataclass

from turboself import consts


@dataclass
class Day:
    eat: bool
    date: datetime
    can_eat: bool

@dataclass
class Week:
    days: list[Day]
    date: datetime

@dataclass
class Event:
    name: str
    date: datetime
    value: str | int | float


class Client:
    def __init__(self,
                 username: str,
                 password: str,
                 login: bool = True,
                 debug: bool = False) -> None:
        '''
        Represensts a TurboSelf client.
        
        Arguments
            username: The client email email/address.
            password: The client clear password.
            login: Whether to immediatly login.
            debug: Whether to print debug to stdout.
        '''
        
        assert len(username) and len(password), 'Invalid credentials'
        
        self.root = 'https://espacenumerique.turbo-self.com/'
        self.session = requests.Session()
        self.debug = debug
        
        self.credentials = {
            'ctl00$cntForm$txtLogin': username,
            'ctl00$cntForm$txtMotDePasse': password
        }
        
        self.cache = {}
        self.credits_cache = []
        
        if login: self.login()
    
    def login(self) -> None:
        '''
        Attempts to login to the target.
        If fails, raises ConnectionError.
        '''
        
        # Load the home page
        if self.debug: print('[LOGIN] Fetching connection page')
        
        homepage = self.session.get(self.root + 'Connexion.aspx')
        
        if self.debug: print('[LOGIN] Sending credentials')
        
        # Build the payload
        data = consts.re.get_home_data(homepage.text)
        payload = {k: v for k, v in data}
        
        # Send authentification
        authpage = self.session.post(self.root + 'Connexion.aspx',
                                     data = payload | self.credentials)
        
        # Verify we are authentificated
        if b'login' in authpage.content:
            raise ConnectionError('Failed to connect, check your credentials.')
    
        if self.debug: print('[LOGIN] Authentificated')
        
    def get(self, page: str, method = 'GET') -> requests.Response:
        '''
        Fetch a page from the target.
        Uses a cache system.
        
        Arguments
            page: the name of the page to fetch
            method: the request type (GET, POST, etc.)
        
        Returns a request response object.
        '''
        
        key = method + ':' + page
        
        # Get in the cache
        if key in self.cache:
            if self.debug: print('[ GET ] Using cached request')
            return self.cache[key]

        # Send the request
        req = self.session.request(method, self.root + page + '.aspx')

        # Error protection
        assert req.ok

        # Save in the cache
        self.cache[key] = req
        return req
    
    def clear_cache(self) -> None:
        '''
        Clear all the cached elements.
        Forces any future client call to update
        the pages it parses.
        '''
        
        self.cache.clear()
        self.credits_cache.clear()
    
    def get_reservations(self) -> Generator[Week, None, None]:
        '''
        Get all programmed reservations by weeks.
        
        Yield Weeks objects containing Day objects.
        '''
        
        # Fetch the raw page
        if self.debug: print('[RESRV] Fetching reservations page')
        raw = self.get('ReserverRepas').content
        
        # Get the weeks
        weeks = Soup(raw, 'html.parser').find_all('div', {'class': 'semaine'})
        if self.debug: print(f'[RESRV] Parsing {len(weeks)} weeks')
        
        for week in weeks:
            
            # Get all days for that week
            days = week.find_all('li', {'class': 'day_line'})
            
            week_object = Week([], None)
            
            for day in days:
                
                # Get data
                day_date = day.find('input', {'class': 'chkDay'})
                day_meal = day.find('label', {'class': 'nbRepas'})
                
                # Avoid header titles
                if day_date is None: continue
                
                day_date = datetime.strptime(day_date.get('id'), '%d%m%Y')
                
                reserved = False if day_meal is None else bool(int(day_meal.text))
                can_eat = day_meal is not None
                
                # Add the week date
                if week_object.date is None:
                    week_object.date = day_date
                
                # Append to the week
                week_object.days.append(Day(reserved, day_date, can_eat))
            
            yield week_object
    
    def get_qr_code(self) -> bytes:
        '''
        Get the QR code image.
        
        Returns the QR code data as bytes.
        '''
        
        # TODO
        # NOTE QR codes are not sent as images from the server
        # so need to reverse the qrcode script or
        # use requests_html.
        
        return
    
    def get_credits(self) -> list[float, int, float]:
        '''
        Get informations on the client credits.
        
        Returns a list containing:
            - The left credits on the account,
            - Its representation in meals,
            - The unit price of one meal.
        '''
        
        if self.debug: print('[CREDS] Fetching credits page')
        raw = self.get('CrediterCompte').text
        
        credits = map(''.join, consts.re.get_credits(raw))
        credits = [float(c.replace(',', '.'))
                   if ',' in c else int(c)
                   for c in credits][:-1]
        
        self.credits_cache = credits
        return credits

    def get_history(self) -> Generator[Event, None, None]:
        '''
        Get the global account history.
        
        Yield Event objects.
        '''
        
        if self.debug: print('[HSTRY] Fetching history page')
        raw = self.get('Accueil').content
        
        # Parse each history line
        lines = Soup(raw, 'html.parser').find_all('tr', {'class': 'rowHistoStyle'})
        if self.debug: print(f'[HSTRY] Parsing {len(lines)} history events')
        
        for line in lines:
            tds = line.find_all('td')
            
            value = tds[1].find('span').text
            name = tds[1].text.replace(value, '')
            date = datetime.strptime(tds[0].text, '%d/%m/%Y - %H:%M')
            
            yield Event(name, date, float(value.replace(',', '.')))
    
    def get_user_data(self) -> dict[str]:
        '''
        Get all disponible user data.
        
        Returns a dict whith parsed target keys and raw values.
        '''
        
        if self.debug: print('[UDATA] Fetching user data page')
        raw = self.get('Accueil').content
        
        # Parse page
        lines = Soup(raw, 'html.parser').find('div', {'class': 'modal-body'})\
            .find_all('span')
        
        if self.debug: print(f'[UDATA] Parsing {len(lines)} data entries')
        
        data = {}

        for line in lines:
            if data_id := line.get('id'):
                key = consts.re.get_user_key(data_id)[0]
                data[key] = line.text
        
        return data
    
    @property
    def credits(self) -> float:
        '''
        The number of credits left on the account.
        '''
        
        if not len(self.credits_cache): self.get_credits()
        return self.credits_cache[0]
    
    @property
    def meals_left(self) -> int:
        '''
        The number of meals left according to the left credits.
        '''
        
        if not len(self.credits_cache): self.get_credits()
        return self.credits_cache[1]
    
    @property
    def unit_price(self) -> float:
        '''
        The price of one meal.
        '''
        
        if not len(self.credits_cache): self.get_credits()
        return self.credits_cache[2]

# EOF