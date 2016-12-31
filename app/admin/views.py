from .. import admin
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView


class CustomView(BaseView):
    """View function of Flask-Admin for Custom page."""

    @expose('/')
    def index(self):
        return self.render('admin/index.html')



class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    pass