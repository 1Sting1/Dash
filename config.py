import sys
path = '/home/your_username/for_study/for_viz/dash'
if path not in sys.path:
    sys.path.insert(0, path)

from dash_app import app
application = app.server
# Реализовано через pythonanywhere