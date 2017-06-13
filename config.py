import os

prod_env = dict(
    DARKSKY_API_KEY=os.environ.get('API_KEY'),
    GEONAMES_USERNAME=os.environ.get('GEONAMES_USERNAME')
)

dev_env = dict(
    DARKSKY_API_KEY=os.environ.get('API_KEY'),
    GEONAMES_USERNAME=os.environ.get('GEONAMES_USERNAME')
)
