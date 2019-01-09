"""Presentations controller"""
from tg import expose, validate, tmpl_context, flash, redirect
from sprox.formbase import AddRecordForm
import tw2.core as twc
import tw2.forms as twf

from acmwebsite.model import DBSession
from acmwebsite.model.presentation import Presentation
from acmwebsite.model.auth import User
from acmwebsite.model.presentation import Presentation, PresentationFile
from acmwebsite.lib.base import BaseController

__all__ = ['PresentationsController']


# WIP
class MultiFileField(twf.widgets.FormField):
    inline_engine_name = 'kajiki'
    template = '''
    <div id="${w.id}">
        <input type="file" />
        <input type="submit" value="Add file" />
    </div>
    '''


class NewPresentationForm(AddRecordForm):
    __model__ = Presentation
    __require_fields__ = ['title', 'date']
    repo_url = twf.UrlField('repo_url')
    files = MultiFileField('files')
new_presentation_form = NewPresentationForm(DBSession)


class PresentationsController(BaseController):
    @expose('acmwebsite.templates.presentations')
    def index(self):
        """List all presentations"""
        presentations = list(DBSession.query(Presentation))
        presentations.sort(key=lambda p: p.date, reverse=True)

        return dict(page='presentations', presentations=presentations)

    @expose('acmwebsite.templates.presentation_upload')
    def upload_form(self, **kw):
        tmpl_context.form = new_presentation_form
        return dict(value=kw)

    @validate(new_presentation_form, error_handler=upload_form)
    @expose()
    def upload(self, **kw):
        del kw['sprox_id']  # required by sprox
        kw['authors'] = [DBSession.query(User).get(id) for id in kw['authors']]
        kw['files'] = [DBSession.query(PresentationFile).get(id) for id in kw['files']]
        pres = Presentation(**kw)
        for f in kw['files']:
            f.presentation_id = pres.id
        DBSession.add(pres)
        flash('Your presentation was successfully uploaded')
        redirect('/index')
