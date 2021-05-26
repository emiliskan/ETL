from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
application = WhiteNoise(application, root='./static')
