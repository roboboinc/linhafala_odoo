# LFC - Assistance

LFC - Assistance is an Odoo module developed in Python by Robobo Inc. for the Linha Fala Criança App.

## System Requirements:
- Odoo Platform Installed;
- Python Dependencies Installed;
- wkhtmltopdf Dependencies for PDF reading;

For more information, please refer to:

- [Odoo documentation](https://www.odoo.com/documentation/16.0/)
- [wkhtmltopdf Downloads](https://wkhtmltopdf.org/downloads.html)

## Deployment commands
docker swarm status

- To remove the stack for restart
 `docker stack rm odoostack`

 - To start it back again
`docker stack deploy --compose-file docker-compose.yml odoostack`
