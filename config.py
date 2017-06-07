import os

prod_env = dict(
    DARKSKY_API_KEY=os.environ.get('API_KEY'),
	SECRET_KEY=os.environ.get('SECRET_KEY')
)
