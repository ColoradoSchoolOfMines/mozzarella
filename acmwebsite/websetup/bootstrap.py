# -*- coding: utf-8 -*-
"""Seed the Mozzarella database"""
import transaction
from acmwebsite import model


def bootstrap(command, conf, vars):
    # <websetup.bootstrap.before.auth>
    from sqlalchemy.exc import IntegrityError
    try:
        jack = model.User(
                user_id=28263,
                user_name="jrosenth",
                display_name="Jack Rosenthal")
        model.DBSession.add(jack)

        sam = model.User(
                user_id=250449,
                user_name="ssartor",
                display_name="Sam Sartor")
        model.DBSession.add(sam)

        sumner = model.User(
                user_id=293299,
                user_name="jonathanevans",
                display_name="Sumner Evans")
        model.DBSession.add(sumner)

        g = model.Group()
        g.group_name = 'officers'
        g.display_name = 'Officers'

        g.users.extend([jack, sam, sumner])
        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = 'admin'
        p.description = 'This permission gives an administrative right'
        p.groups.append(g)
        model.DBSession.add(p)

        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
