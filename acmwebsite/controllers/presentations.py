"""Presentations controller"""
from datetime import datetime

from tg import expose, validate, tmpl_context, flash, redirect, require
from tg.predicates import not_anonymous
from formencode.validators import RequireIfPresent
from formencode.schema import Schema
from sprox.formbase import AddRecordForm
import tw2.forms as twf

from acmwebsite.model import DBSession
from acmwebsite.model.presentation import Presentation, PresentationFile
from acmwebsite.model.auth import User
from acmwebsite.lib.base import BaseController

__all__ = ['PresentationsController']


form_validator = Schema(allow_extra_fields=True,
                        chained_validators=[RequireIfPresent('file_description', present='file'),
                                            RequireIfPresent('file_2_description', present='file_2'),
                                            RequireIfPresent('file_3_description', present='file_3')])


class NewPresentationForm(AddRecordForm):
    __model__ = Presentation
    __require_fields__ = ['title', 'date']
    __omit_fields__ = ['files']
    __field_order__ = ['title', 'description', 'date', 'thumbnail', 'repo_url',
                       'authors', 'file', 'file_description', 'file_2',
                       'file_2_description', 'file_3', 'file_3_description']
    __base_validator__ = form_validator
    repo_url = twf.UrlField('repo_url')
    # this sucks, but I can't figure out a cleaner, simpler way of doing it
    file = twf.FileField('file')
    file_description = twf.TextField('file_description')
    file_2 = twf.FileField('file_2')
    file_2_description = twf.TextField('file_2_description')
    file_3 = twf.FileField('file_3')
    file_3_description = twf.TextField('file_3_description')
new_presentation_form = NewPresentationForm(DBSession)


class PresentationsController(BaseController):
    @expose('acmwebsite.templates.presentations')
    def index(self):
        """List all presentations"""
        presentations = list(DBSession.query(Presentation))
        presentations.sort(key=lambda p: p.date, reverse=True)

        return dict(page='presentations', presentations=presentations)

    @expose('acmwebsite.templates.presentation_upload')
    @require(not_anonymous(msg='Only logged in users can sumbit presentations'))
    def upload_form(self, **kw):
        tmpl_context.form = new_presentation_form
        return dict(page='presentation_upload', value=kw)

    @validate(new_presentation_form, error_handler=upload_form)
    @expose()
    @require(not_anonymous(msg='Only logged in users can sumbit presentations'))
    def upload(self, **kw):
        del kw['sprox_id']  # required by sprox
        kw['authors'] = [DBSession.query(User).get(id) for id in kw['authors']]

        pres = Presentation()

        kw['files'] = []
        for f in ('file', 'file_2', 'file_3'):
            if kw[f] is not None:
                print('ohea', kw)
                kw['files'].append(PresentationFile(presentation_id=pres.id,
                                                    file=kw[f],
                                                    description=kw['{}_description'.format(f)]))
                DBSession.add(kw['files'][-1])
            del kw[f]
            del kw['{}_description'.format(f)]

        for k, v in kw.items():
            setattr(pres, k, v)
        DBSession.add(pres)
        DBSession.flush()

        flash('Your presentation was successfully uploaded')
        redirect('/presentations')
