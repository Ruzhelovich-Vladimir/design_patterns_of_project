def secret_front(request):
    request['secret'] = 'some secret'


def user_info_front(request):
    request['user'] = {}
    request['user']['username'] = 'Same user'
    request['user']['age'] = '25'
