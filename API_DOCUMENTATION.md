# Linha Fala Criança REST API Documentation

## Authentication

All API requests require authentication using an API key. Include the API key in the request header:

```
X-API-Key: your_api_key_here
```

## Creating API Keys

1. Log in to Odoo as an Administrator or Gestor
2. Navigate to **Configuration → API Keys**
3. Click **Create**
4. Fill in:
   - **Key Name**: Descriptive name (e.g., "Partner XYZ Integration")
   - **Associated User**: Select a user account (API requests will run with this user's permissions)
   - **Expires At** (optional): Set expiration date
   - **Allowed IPs** (optional): Restrict access to specific IP addresses
5. Click **Save**
6. Copy the generated API key (you can view it by clicking the eye icon)

⚠️ **Important**: Store the API key securely. It provides access to create records in your system.

## Endpoints

### Health Check

Test if the API is available.

**Endpoint:** `GET /api/v1/caso/health`

**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "service": "Linha Fala Caso API",
  "version": "1.0"
}
```

### Create Caso

Create a new Caso record.

**Endpoint:** `POST /api/v1/caso/create`

**Headers:**
- `Content-Type: application/json`
- `X-API-Key: your_api_key_here`

**Request Body:**

```json
{
  "call_id": 0,
  "case_priority": "Urgente",
  "case_type": "caso de natureza criminal",
  "secundary_case_type": "outros tipos de crimes",
  "case_type_classification": "Grave",
  "place_occurrence": "Escola",
  "case_handling": "Aconselhamento LFC",
  "created_by": "API Integration",
  "detailed_case_description": "Detailed description of the case...",
  "person_id": [
    {
      "person_type": "Vítima",
      "fullname": "João Silva",
      "gender": "Masculino",
      "age": 15,
      "contact": "+258 84 123 4567",
      "provincia": "Maputo Cidade",
      "distrito": "Kamavota",
      "victim_relationship": "Nenhuma"
    },
    {
      "person_type": "Contactante",
      "fullname": "Maria Silva",
      "gender": "Feminino",
      "age": 24,
      "contact": "+258 84 765 4321",
      "provincia": "Maputo Cidade",
      "distrito": "Kamavota",
      "victim_relationship": "Mãe"
    }
  ]
}
```

**Required Fields:**
- `case_priority`: One of: "Muito Urgente", "Urgente", "Moderado", "Não Aplicável"
- `case_type`: String (case category name, e.g., "Abuso Físico") or Integer (ID)
- `secundary_case_type`: String (sub-category name) or Integer (ID)
- `case_type_classification`: String (classification name) or Integer (ID)
- `place_occurrence`: One of: "Escola", "Casa propria", "Casa do vizinho", "Cresce/infantário", "Casa do parente mais próximo", "Outros"
- `case_handling`: One of: "Aconselhamento LFC", "Encaminhado", "Não encaminhado"
- `detailed_case_description`: String (will be converted to detailed_description records)
- `person_id`: Array with at least one person of type "Vítima" or "Contactante+Vítima", AND at least one person of type "Contactante" or "Contactante+Vítima"

**Person Object Fields:**
Each person in the `person_id` array requires:
- `person_type`: One of: "Vítima", "Contactante", "Contactante+Vítima", "Agressor", "Testemunha"
- `fullname`: String
- `gender`: String (e.g., "Masculino", "Feminino")
- `age`: Integer or String (will be converted to string)
- `provincia`: String (province name, e.g., "Maputo Cidade") or Integer (province ID) - **REQUIRED**
- `victim_relationship`: String - **REQUIRED**. One of: "Pai", "Mãe", "Avo", "Amigo", "Outros", "Colega", "Esposo", "Tio(a)", "Nenhuma", "Mentora", "Irmã(o)", "Primo(a)", "Namorado", "Madrasta", "Padrasto", "Empregador", "Vizinho (a)", "Denunciante", "Educador(a)", "Professor(a)", "Não aplicavél"

Optional person fields:
- `contact`: String (phone number)
- `distrito`: String (district name) or Integer (ID)
- `posto`: String or Integer (ID)
- `localidade`: String or Integer (ID)
- `address`: String

**Available Provinces:**
- Maputo Cidade
- Maputo Provincia
- Gaza
- Inhambane
- Sofala
- Manica
- Tete
- Zambezia
- Nampula
- Niassa
- Cabo Delgado

**Optional Fields:**
- `call_id`: Integer (reference to a Chamada record)
- `created_by`: String (username or name) or Integer (user ID)
- `data_ocorrencia`: String (ISO format datetime)
- `online_offline`: One of: "Online", "Offline" (required if case_type is criminal)
- `case_status`: One of: "Aberto/Pendente", "Dentro do sistema", "Assistido", "No Arquivo Morto", "Encerrado" (defaults to "Aberto/Pendente")
- `inqueritos_id`: Array of inquerito objects

**Success Response (201 Created):**
```json
{
  "success": true,
  "caso_id": "CASO-00123",
  "id": 123,
  "message": "Caso created successfully"
}
```

**Error Responses:**

**401 Unauthorized:**
```json
{
  "error": true,
  "message": "Invalid or missing API key",
  "code": "INVALID_API_KEY"
}
```

**400 Bad Request:**
```json
{
  "error": true,
  "message": "Invalid JSON: Expecting value: line 1 column 1 (char 0)",
  "code": "INVALID_JSON"
}
```

**422 Unprocessable Entity:**
```json
{
  "error": true,
  "message": "Porfavor adicione uma 'Vitima' ou 'Contactante+Vitima' para prosseguir.",
  "code": "VALIDATION_ERROR"
}
```

### Get Caso

Retrieve a Caso record by ID.

**Endpoint:** `GET /api/v1/caso/<caso_id>`

**Headers:**
- `X-API-Key: your_api_key_here`

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "case_id": "CASO-00123",
    "call_id": 456,
    "case_priority": "Urgente",
    "case_type": "Abuso Físico",
    "secundary_case_type": "Violência Doméstica",
    "created_by": "John Doe",
    "detailed_case_description": "Description...",
    "case_status": "Aberto/Pendente",
    "create_date": "2025-12-08 10:30:00",
    "write_date": "2025-12-08 14:45:00"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "error": true,
  "message": "Caso not found",
  "code": "NOT_FOUND"
}
```

## Example Usage

### cURL

```bash
# Health check
curl https://your-odoo-domain.com/api/v1/caso/health

# Create caso
curl -X POST https://your-odoo-domain.com/api/v1/caso/create \
  -H "Content-Type: application/json" \
  -H "X-API-Key: lfk_your_api_key_here" \
  -d '{
    "case_priority": "Urgente",
    "case_type": "Abuso Físico",
    "secundary_case_type": "Violência Doméstica",
    "case_type_classification": "Grave",
    "place_occurrence": "Escola",
    "case_handling": "Aconselhamento LFC",
    "created_by": "Partner API",
    "detailed_case_description": "Case details here",
    "person_id": [
      {
        "person_type": "Vítima",
        "fullname": "João Silva",
        "gender": "Masculino",
        "age": 15,
        "provincia": "Maputo Cidade",
        "victim_relationship": "Nenhuma"
      },
      {
        "person_type": "Contactante",
        "fullname": "Maria Silva",
        "gender": "Feminino",
        "age": 45,
        "provincia": "Maputo Cidade",
        "victim_relationship": "Mãe"
      }
    ]
  }'

# Get caso
curl https://your-odoo-domain.com/api/v1/caso/123 \
  -H "X-API-Key: lfk_your_api_key_here"
```

### Python

```python
import requests

API_URL = "https://your-odoo-domain.com/api/v1/caso"
API_KEY = "lfk_your_api_key_here"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# Create caso
data = {
    "case_priority": "Urgente",
    "case_type": "Abuso Físico",
    "secundary_case_type": "Violência Doméstica",
    "case_type_classification": "Grave",
    "place_occurrence": "Escola",
    "case_handling": "Aconselhamento LFC",
    "created_by": "Partner API",
    "detailed_case_description": "Case details",
    "person_id": [
        {
            "person_type": "Vítima",
            "fullname": "João Silva",
            "gender": "Masculino",
            "age": 15,
            "provincia": "Maputo Cidade",
            "victim_relationship": "Nenhuma"
        },
        {
            "person_type": "Contactante",
            "fullname": "Maria Silva",
            "gender": "Feminino",
            "age": 45,
            "provincia": "Maputo Cidade",
            "victim_relationship": "Mãe"
        }
    ]
}

response = requests.post(
    f"{API_URL}/create",
    json=data,
    headers=headers
)

if response.status_code == 201:
    result = response.json()
    print(f"Caso created: {result['caso_id']}")
else:
    print(f"Error: {response.json()}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_URL = 'https://your-odoo-domain.com/api/v1/caso';
const API_KEY = 'lfk_your_api_key_here';

const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': API_KEY
};

// Create caso
const data = {
  case_priority: 'Urgente',
  case_type: 'Abuso Físico',
  secundary_case_type: 'Violência Doméstica',
  case_type_classification: 'Grave',
  place_occurrence: 'Escola',
  case_handling: 'Aconselhamento LFC',
  created_by: 'Partner API',
  detailed_case_description: 'Case details',
  person_id: [
    {
      person_type: 'Vítima',
      fullname: 'João Silva',
      gender: 'Masculino',
      age: 15,
      provincia: 'Maputo Cidade',
      victim_relationship: 'Nenhuma'
    },
    {
      person_type: 'Contactante',
      fullname: 'Maria Silva',
      gender: 'Feminino',
      age: 45,
      provincia: 'Maputo Cidade',
      victim_relationship: 'Mãe'
    }
  ]
};

axios.post(`${API_URL}/create`, data, { headers })
  .then(response => {
    console.log('Caso created:', response.data.caso_id);
  })
  .catch(error => {
    console.error('Error:', error.response.data);
  });
```

## Security Best Practices

1. **Keep API keys secret**: Never commit API keys to version control
2. **Use HTTPS**: Always use HTTPS in production
3. **Rotate keys regularly**: Regenerate API keys periodically
4. **Limit permissions**: Associate API keys with users that have minimal required permissions
5. **Set expiration dates**: Use expiration dates for temporary integrations
6. **Restrict IPs**: When possible, restrict API access to known IP addresses
7. **Monitor usage**: Review API key usage logs regularly
8. **Revoke compromised keys**: Immediately revoke any suspected compromised keys

## Rate Limiting

Currently, there is no rate limiting implemented. Consider implementing rate limiting based on your usage patterns.

## Support

For technical support or questions, contact: team@robobo.org
