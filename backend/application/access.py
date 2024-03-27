from application.db import User, Approval, Section
from application.cache import cache


@cache.memoize()
def acs_user_all():
    return User.query.all()

@cache.memoize()
def acs_approval_with_status(status):
    return Approval.query.filter_by(status=status).all()

@cache.memoize()
def acs_section_all():
    return Section.query.all()
