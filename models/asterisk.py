from odoo import fields, models, api


class Asterisk(models.Model):
    _name = "linhafala.asterisk"
    _description = "Asterisk Agent"

    asterisk_id = fields.Char(string="ID do Asterisk", readonly=True)

    time = fields.Datetime()
    callerIDName = fields.Char()
    callerIDNum = fields.Char()
    channel = fields.Char()
    channelState = fields.Char()
    channelStateDesc = fields.Char()
    connectedLineName = fields.Char()
    connectedLineNum = fields.Char()
    event = fields.Char()
    exten = fields.Char()
    linkedid = fields.Char()
    uniqueid = fields.Char()

    @api.model
    def handleEvent(self, event):
        get = event['headers'].get
        data = {
            'time': get('$time'),
            'callerIDName': get('CallerIDName'),
            'callerIDNum': get('CallerIDNum'),
            'channel': get('Channel'),
            'channelState': get('ChannelState'),
            'connectedLineName': get('ConnectedLineName'),
            'connectedLineNum': get('ConnectedLineNum'),
            'event': get('Event'),
            'exten': get('Exten'),
            'linkedid': get('Linkedid'),
            'uniqueid': get('Uniqueid')
        }
        return data