# -*- coding: utf-8 -*-
import json
import logging
from odoo import http, fields, api
from odoo.http import request, Response
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CasoAPIController(http.Controller):
    """REST API for creating Caso records with API key authentication"""

    def _validate_api_key(self, api_key):
        """Validate API key and return the associated user"""
        if not api_key:
            return None
        
        ApiKey = request.env['linhafala.api.key'].sudo()
        key_record = ApiKey.search([
            ('key', '=', api_key),
            ('active', '=', True)
        ], limit=1)
        
        if key_record and key_record.is_valid():
            # Log API usage
            key_record.sudo().write({
                'last_used': fields.Datetime.now(),
                'usage_count': key_record.usage_count + 1
            })
            return key_record.user_id
        return None

    def _json_response(self, data, status=200):
        """Return a JSON response"""
        return Response(
            json.dumps(data, ensure_ascii=False, default=str),
            status=status,
            mimetype='application/json',
            headers=[('Content-Type', 'application/json; charset=utf-8')]
        )

    def _error_response(self, message, status=400, error_code=None):
        """Return an error response"""
        error_data = {
            'error': True,
            'message': message
        }
        if error_code:
            error_data['code'] = error_code
        return self._json_response(error_data, status=status)

    @http.route('/api/v1/caso/create', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def create_caso(self, **kwargs):
        """
        Create a new Caso record
        
        Headers:
            X-API-Key: Your API key
            
        Request Body (JSON):
        {
            "call_id": "string (optional)",
            "case_priority": "string (Muito Urgente/Urgente/Moderado/Baixa)",
            "case_type": "string",
            "secundary_case_type": "string",
            "case_type_classification": "string or int (id)",
            "created_by": "string",
            "detailed_case_description": "string",
            "person_id": [
                {
                    "person_type": "Vítima/Contactante/Contactante+Vítima",
                    "fullname": "string",
                    "gender": "string",
                    "age": int,
                    ... other person fields
                }
            ],
            ... other caso fields
        }
        
        Response:
        {
            "success": true,
            "caso_id": "CASO-XXXXX",
            "id": 123,
            "message": "Caso created successfully"
        }
        """
        try:
            # Get API key from header
            api_key = request.httprequest.headers.get('X-API-Key')
            
            # Validate API key
            user = self._validate_api_key(api_key)
            if not user:
                return self._error_response(
                    'Invalid or missing API key',
                    status=401,
                    error_code='INVALID_API_KEY'
                )
            
            # Parse JSON body
            try:
                data = json.loads(request.httprequest.data.decode('utf-8'))
            except (ValueError, json.JSONDecodeError) as e:
                return self._error_response(
                    f'Invalid JSON: {str(e)}',
                    error_code='INVALID_JSON'
                )
            
            # Validate required fields
            if not data:
                return self._error_response(
                    'Request body cannot be empty',
                    error_code='EMPTY_BODY'
                )
            
            # Normalize some incoming fields so clients can send human-friendly values
            # and the controller will resolve them to the proper database ids/commands.
            # Create a new environment with the authenticated user
            env = api.Environment(request.cr, user.id, {})

            # Helper: resolve a Many2one value received as a string to an ID
            def _resolve_m2o(field_val, model_name, name_field='name'):
                if not field_val:
                    return False
                # already an int id
                if isinstance(field_val, int):
                    return field_val
                # if client sent a dict command or tuple, pass through
                if isinstance(field_val, (list, tuple)):
                    return field_val
                # assume a human-readable name was provided -> try to find record
                rec = env[model_name].search([(name_field, 'ilike', str(field_val))], limit=1)
                return rec.id if rec else False

            # Map many2one string names to ids for known fields
            # case_type -> linhafala.caso.categoria
            if 'case_type' in data and data.get('case_type'):
                resolved = _resolve_m2o(data.get('case_type'), 'linhafala.caso.categoria')
                if resolved:
                    data['case_type'] = resolved
                # If not resolved and it's not already an int, we have a problem
                elif not isinstance(data.get('case_type'), int):
                    return self._error_response(
                        f"Invalid case_type: '{data.get('case_type')}'. Could not find matching category.",
                        status=400,
                        error_code='INVALID_CASE_TYPE'
                    )

            # secundary_case_type -> linhafala.caso.subcategoria
            if 'secundary_case_type' in data and data.get('secundary_case_type'):
                resolved = _resolve_m2o(data.get('secundary_case_type'), 'linhafala.caso.subcategoria')
                if resolved:
                    data['secundary_case_type'] = resolved
                elif not isinstance(data.get('secundary_case_type'), int):
                    return self._error_response(
                        f"Invalid secundary_case_type: '{data.get('secundary_case_type')}'. Could not find matching sub-category.",
                        status=400,
                        error_code='INVALID_SECUNDARY_CASE_TYPE'
                    )

            # case_type_classification -> linhafala.caso.case_type_classification
            if 'case_type_classification' in data and data.get('case_type_classification'):
                resolved = _resolve_m2o(data.get('case_type_classification'), 'linhafala.caso.case_type_classification')
                if resolved:
                    data['case_type_classification'] = resolved
                elif not isinstance(data.get('case_type_classification'), int):
                    return self._error_response(
                        f"Invalid case_type_classification: '{data.get('case_type_classification')}'. Could not find matching classification.",
                        status=400,
                        error_code='INVALID_CLASSIFICATION'
                    )

            # created_by -> res.users (accept login or name)
            if 'created_by' in data and data.get('created_by'):
                created_by_val = data.get('created_by')
                if isinstance(created_by_val, int):
                    data['created_by'] = created_by_val
                else:
                    u = env['res.users'].search([('login', '=', str(created_by_val))], limit=1)
                    if not u:
                        u = env['res.users'].search([('name', 'ilike', str(created_by_val))], limit=1)
                    if u:
                        data['created_by'] = u.id
                    else:
                        # Remove created_by if not resolvable (model default will set env.user)
                        data.pop('created_by', None)

            # If client sent a free-text description field, convert it into a One2many command
            # The model expects `detailed_description` One2many to lin hafala.caso.description (field 'content')
            if 'detailed_case_description' in data and data.get('detailed_case_description'):
                desc_text = data.pop('detailed_case_description')
                if isinstance(desc_text, str) and desc_text.strip():
                    data['detailed_description'] = [(0, 0, {
                        'content': desc_text,
                        'created_by': env.uid,
                    })]

            # Normalize person ages (model stores ages as strings in a selection)
            # Also resolve provincia and distrito names to IDs
            person_data = data.pop('person_id', [])  # Pop here so we work with the actual data
            if isinstance(person_data, list):
                for p in person_data:
                    if p is None:
                        continue
                    # if age is numeric, convert to string (selection stores strings)
                    if 'age' in p and isinstance(p.get('age'), (int, float)):
                        p['age'] = str(int(p.get('age')))
                    
                    # Resolve provincia if provided as string
                    if 'provincia' in p and p.get('provincia'):
                        if isinstance(p.get('provincia'), str):
                            prov_id = _resolve_m2o(p.get('provincia'), 'linhafala.provincia')
                            if prov_id:
                                p['provincia'] = prov_id
                            else:
                                return self._error_response(
                                    f"Invalid provincia: '{p.get('provincia')}' for person '{p.get('fullname', 'unknown')}'. Could not find matching province.",
                                    status=400,
                                    error_code='INVALID_PROVINCIA'
                                )
                    
                    # Resolve distrito if provided as string
                    if 'distrito' in p and p.get('distrito'):
                        if isinstance(p.get('distrito'), str):
                            dist_id = _resolve_m2o(p.get('distrito'), 'linhafala.distrito')
                            if dist_id:
                                p['distrito'] = dist_id
                            else:
                                return self._error_response(
                                    f"Invalid distrito: '{p.get('distrito')}' for person '{p.get('fullname', 'unknown')}'. Could not find matching district.",
                                    status=400,
                                    error_code='INVALID_DISTRITO'
                                )
                    
                    # Validate posto is provided (REQUIRED)
                    if 'posto' not in p or not p.get('posto'):
                        return self._error_response(
                            f"posto is required for person '{p.get('fullname', 'unknown')}'",
                            status=400,
                            error_code='MISSING_POSTO'
                        )
                    
                    # Resolve posto if provided as string
                    if isinstance(p.get('posto'), str):
                        posto_id = _resolve_m2o(p.get('posto'), 'linhafala.posto')
                        if posto_id:
                            p['posto'] = posto_id
                        else:
                            return self._error_response(
                                f"Invalid posto: '{p.get('posto')}' for person '{p.get('fullname', 'unknown')}'. Could not find matching posto.",
                                status=400,
                                error_code='INVALID_POSTO'
                            )
                    
                    # Validate localidade is provided (REQUIRED)
                    if 'localidade' not in p or not p.get('localidade'):
                        return self._error_response(
                            f"localidade is required for person '{p.get('fullname', 'unknown')}'",
                            status=400,
                            error_code='MISSING_LOCALIDADE'
                        )
                    
                    # Resolve localidade if provided as string
                    if isinstance(p.get('localidade'), str):
                        localidade_id = _resolve_m2o(p.get('localidade'), 'linhafala.localidade')
                        if localidade_id:
                            p['localidade'] = localidade_id
                        else:
                            return self._error_response(
                                f"Invalid localidade: '{p.get('localidade')}' for person '{p.get('fullname', 'unknown')}'. Could not find matching localidade.",
                                status=400,
                                error_code='INVALID_LOCALIDADE'
                            )
                    
                    # Validate victim_relationship is provided (required field)
                    if 'victim_relationship' not in p or not p.get('victim_relationship'):
                        return self._error_response(
                            f"victim_relationship is required for person '{p.get('fullname', 'unknown')}'",
                            status=400,
                            error_code='MISSING_VICTIM_RELATIONSHIP'
                        )
                    
                    # Set are_you_disabled to "Não" if not provided (required field)
                    if 'are_you_disabled' not in p or not p.get('are_you_disabled'):
                        p['are_you_disabled'] = 'Não'

            # Create caso with the authenticated user's context
            Caso = env['linhafala.caso']
            
            # Process person_id - convert to One2many commands using normalized data
            person_commands = []
            for person in person_data:
                person_commands.append((0, 0, person))

            if person_commands:
                data['person_id'] = person_commands
            
            # Process inqueritos_id if provided
            inqueritos_data = data.pop('inqueritos_id', [])
            inqueritos_commands = []
            for inquerito in inqueritos_data:
                inqueritos_commands.append((0, 0, inquerito))
            
            if inqueritos_commands:
                data['inqueritos_id'] = inqueritos_commands
            
            # Create the caso record
            caso = Caso.create(data)
            
            return self._json_response({
                'success': True,
                'caso_id': caso.case_id,
                'id': caso.id,
                'message': 'Caso created successfully'
            }, status=201)
            
        except ValidationError as e:
            return self._error_response(
                str(e),
                status=422,
                error_code='VALIDATION_ERROR'
            )
        except Exception as e:
            _logger.exception("Error creating caso via API")
            return self._error_response(
                f'Internal server error: {str(e)}',
                status=500,
                error_code='INTERNAL_ERROR'
            )

    @http.route('/api/v1/caso/<int:caso_id>', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_caso(self, caso_id, **kwargs):
        """
        Get a Caso record by ID
        
        Headers:
            X-API-Key: Your API key
        """
        try:
            # Get API key from header
            api_key = request.httprequest.headers.get('X-API-Key')
            
            # Validate API key
            user = self._validate_api_key(api_key)
            if not user:
                return self._error_response(
                    'Invalid or missing API key',
                    status=401,
                    error_code='INVALID_API_KEY'
                )
            
            # Get caso record using the API key's user context
            env = api.Environment(request.cr, user.id, {})
            Caso = env['linhafala.caso']
            caso = Caso.browse(caso_id)
            
            if not caso.exists():
                return self._error_response(
                    'Caso not found',
                    status=404,
                    error_code='NOT_FOUND'
                )
            
            # Prepare response data
            caso_data = {
                'id': caso.id,
                'case_id': caso.case_id,
                'call_id': caso.call_id.id if caso.call_id else None,
                'case_priority': caso.case_priority,
                'case_type': caso.case_type,
                'secundary_case_type': caso.secundary_case_type,
                'created_by': caso.created_by.name if caso.created_by else None,
                'detailed_case_description': caso.detailed_case_description,
                'case_status': caso.case_status,
                'create_date': caso.create_date,
                'write_date': caso.write_date,
            }
            
            return self._json_response({
                'success': True,
                'data': caso_data
            })
            
        except Exception as e:
            _logger.exception("Error retrieving caso via API")
            return self._error_response(
                f'Internal server error: {str(e)}',
                status=500,
                error_code='INTERNAL_ERROR'
            )

    @http.route('/api/v1/caso/health', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def health_check(self):
        """Health check endpoint"""
        return self._json_response({
            'status': 'healthy',
            'service': 'Linha Fala Caso API',
            'version': '1.0'
        })
