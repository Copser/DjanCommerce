from fabric.api import local


def commit():
    """TODO: Docstring for commit.
    :returns: TODO

    """
    local('git add .')
    print("Enter your git commit massage: ")
    comment = raw_input()
    local('git commit -m "%s"' % comment)


def prep():
    commit()


def push():
    """TODO: Docstring for push.
    :returns: TODO

    """
    local('git push -u origin master')


def deploy():
    """TODO: Docstring for deploy.
    :returns: TODO

    """
    push()
