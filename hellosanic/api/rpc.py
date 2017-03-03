import os

from sanic import Blueprint
from sanic.response import json


rpc = Blueprint('rpc', url_prefix='/rpc')


@rpc.get('/process')
async def process(request):
    return json({
        'pid': os.getpid(),
        'app': id(request.app),
    })
