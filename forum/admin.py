from flask import abort
from flask.ext.admin import (Admin, BaseView as _BaseView,
                            AdminIndexView as _AdminIndexView,
                             expose)
from flask.ext.admin.contrib.sqlamodel import ModelView as _ModelView
from flask.ext.security import current_user

from app import app
from app import db
from app import models
from forum import models as forum_models
from app import models as app_models


# Base classes
# ------------
class AuthMixin(object):
    def is_accessible(self):
        """Returns ``True`` if `current_user` has access to admin views.
        This method checks whether `current_user` has the ``'admin'``
        role.
        """
        return current_user.is_admin()


class AdminIndexView(_AdminIndexView):
    """An `:class:`~flask.ext.admin.AdminIndexView` with authentication"""
    @expose('/')
    def index(self):
        if current_user.is_admin():
            return self.render(self._template)
        else:
            abort(404)


class BaseView(AuthMixin, _BaseView):
    """A `:class:`~flask.ext.admin.BaseView` with authentication."""
    pass


class ModelView(AuthMixin, _ModelView):
    """A `:class:`~flask.ext.admin.contrib.sqlamodel.ModelView` with
    authentication.
    """
    pass


# Custom views
# ------------
class UserView(ModelView):
    column_exclude_list = form_excluded_columns = ['password']


# Admin setup
# -----------
admin = Admin(name='Index', index_view=AdminIndexView(url='/db_admin/'))

# Forums
admin.add_view(ModelView(forum_models.Board, db.session,
                         category='Forum',
                         name='Boards'))
admin.add_view(ModelView(forum_models.Thread, db.session,
                         category='Forum',
                         name='Threads'))
admin.add_view(ModelView(forum_models.Post, db.session,
                         category='Forum',
                         name='Posts'))
# Users
admin.add_view(UserView(app_models.Users, db.session,
                        category='Users',
                        name='Users'))
admin.add_view(ModelView(models.Watches, db.session,
                         category='Users',
                         name='Watches'))



# Releases
# Language
# classtype,
# Feeds
# FeedAuthors
# FeedTags
# Watches

admin.add_view(ModelView(models.Series, db.session,
                         category='Content',
                         name='Series'))
admin.add_view(ModelView(models.Tags, db.session,
                         category='Content',
                         name='Tags'))
admin.add_view(ModelView(models.Genres, db.session,
                         category='Content',
                         name='Genres'))
admin.add_view(ModelView(models.Author, db.session,
                         category='Content',
                         name='Author'))
admin.add_view(ModelView(models.Illustrators, db.session,
                         category='Content',
                         name='Illustrators'))
admin.add_view(ModelView(models.AlternateNames, db.session,
                         category='Content',
                         name='AlternateNames'))
admin.add_view(ModelView(models.AlternateTranslatorNames, db.session,
                         category='Content',
                         name='AlternateTranslatorNames'))
admin.add_view(ModelView(models.Translators, db.session,
                         category='Content',
                         name='Translators'))
admin.add_view(ModelView(models.Publishers, db.session,
                         category='Content',
                         name='Publishers'))
admin.add_view(ModelView(models.Covers, db.session,
                         category='Content',
                         name='Covers'))
admin.add_view(ModelView(models.Language, db.session,
                         category='Content',
                         name='Language'))




admin.add_view(ModelView(models.Releases, db.session,
                         category='Releases',
                         name='Releases'))

admin.add_view(ModelView(models.News_Posts, db.session,
                         category='News',
                         name='NewsPosts'))




admin.init_app(app)