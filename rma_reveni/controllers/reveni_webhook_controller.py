import json

from odoo.http import request, Controller, route, Response
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }
class ReveniWebhoohController(Controller):

    @route('/reveni/webhook', type='json', auth='public', csrf=False, cors='*', methods=['POST'])
    def webhook(self):
        event_obj = request.env['reveni.event'].sudo()
        if request.jsonrequest and \
                request.jsonrequest.get('data') and \
                request.jsonrequest.get('data',{}).get('status') == 'in_progress':
            try:
                event = event_obj.create({
                    'event_name': request.jsonrequest.get('id'),
                    'event_data': request.jsonrequest.get('data'),
                    'event_date': datetime.fromtimestamp(request.jsonrequest.get('created')).strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'event_type': request.jsonrequest.get('event')
                })
                event.action_process_event()
                return 'OK'
            except Exception as e:
                res = error_response(e, e.msg)
                return Response(status=500,response=json.dumps(res))
        return Response(status=201)
