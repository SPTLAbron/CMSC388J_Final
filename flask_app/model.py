import requests

class Cat(object):
    def __init__(self, cat_json):
        self.id = cat_json['id']
        self.url = cat_json['url']
        self.width = cat_json['width']
        self.height = cat_json['height']

    def __repr__(self):
        return f"{self.id}: {self.url}"

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'width': self.width,
            'height': self.height
        }

class CatClient(object):
    def __init__(self, api_key, limit):
        self.sess = requests.Session()
        self.limit = limit
        self.base_url = f'https://api.thecatapi.com/v1/images/search?limit={limit}'
        self.headers = {'x-api-key': api_key}
    
    def get_all_cats(self):
        cats = []
        resp = self.sess.get(self.base_url, headers=self.headers)
        if resp.status_code != 200:
            raise ValueError('Request failed; make sure your API key is correct and authorized')
            
        data = resp.json()
        cats.extend(Cat(cat).to_dict() for cat in data)
        return cats
    
    def retrieve_cat_by_id(self, cat_id):
        
        movie_url = 'https://api.thecatapi.com/v1/images/' + str(cat_id)

        resp = self.sess.get(movie_url)

        if resp.status_code != 200:
            raise ValueError('Search request failed; make sure your API key is correct and authorized')

        data = resp.json()

        movie = Cat(data)

        return movie

if __name__=='__main__':
    import os
    client = CatClient(os.environ.get('CAT_API_KEY'))
    cat_images = client.get_all_cats()