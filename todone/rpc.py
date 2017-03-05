from sanic import Blueprint
from sanic.response import json


rpc = Blueprint('rpc', url_prefix='/rpc')


@rpc.route('/cookie', methods={'GET', 'POST'})
async def cookie(request):
    # unwrap arg values from array for filter predicate
    response = json("There's a cookie up in this response")
    response.cookies['test'] = 'It worked!'
    return response
