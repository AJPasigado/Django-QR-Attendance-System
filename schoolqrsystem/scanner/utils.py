def is_teacher(user):
    if user:
        return user.groups.filter(name='Teacher').count() > 0 or user.is_superuser
    return False
