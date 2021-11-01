from main import app
from werkzeug.middleware.profiler import ProfilerMiddleware

app.config['PROFILE'] = True

app.wsgi_app = ProfilerMiddleware(
     app.wsgi_app,
     # restrictions=[5000],
     profile_dir='.')

app.run(debug=True)


