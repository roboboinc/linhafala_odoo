from odoo import http
# from models.chamada import Chamada

import json
class OdooAPIController(http.Controller):
    @http.route('/api/endpoint', auth='public', methods=['GET'], type="json", csrf=False)
    def api_endpoint(self, **kw):
        # Access the request parameters
        # parameters = json.loads(http.request.httprequest.data)
        # Process the API request and return the response
        response = {
            'status': 'success',
            'message': 'API request received without authentication',
            'data': {
                'parameters': 'parameters'
            }
        }
        return {'status': 'success', 'id': 1}