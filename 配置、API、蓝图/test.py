# from flask_restful import marshal_with, marshal, fields, Resource
#
# resource_fields = {
#     'name': fields.String,
#     'address': fields.String,
#     'date_updated': fields.DateTime(dt_format='rfc822'),
# }
#
#
# class Todo(Resource):
#     @marshal_with(resource_fields, envelope='resource')
#     def get(self):
#         return {'name': 'yeyuning',
#                 'address': 'yeyuning'}  # Some function that queries the db
#
#     def post(self):
#         data = {'name': 'yeyuning',
#                 'address': 'yeyuning'}
#         return marshal(data, resource_fields, envelope='resource')


# from flask_restful import fields, marshal
# import json
#
# resource_fields = {
#     'name': fields.String,
#     'address': {
#         'line1': fields.String(attribute='addr1'),
#         'line2': fields.String(attribute='addr2'),
#         'city': fields.String,
#         'state': fields.String,
#         'zip': fields.String
#     }
# }
# data = {'name': 'Jason', 'addr1': '123 fake street', 'addr2': '', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
# json.dumps(marshal(data, resource_fields))
# # '{"name": "Jason", "address": {"line 1": "123 street", "line 2": "",
# # "state": "ZJ", "zip": "10008", "city": "HANG ZHOU"}}'


# from flask_restful import fields, marshal
# import json
#
# address_fields = {
#     'line1': fields.String(attribute='addr1'),
#     'line2': fields.String(attribute='addr2'),
#     'city': fields.String(attribute='city'),
#     'state': fields.String(attribute='state'),
#     'zip': fields.String(attribute='zip')
# }
#
# resource_fields = {
#     'name': fields.String,
#     'billing_address': fields.Nested(address_fields),
#     'shipping_address': fields.Nested(address_fields)
# }
#
# address1 = {'addr1': '123 fake street', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
# address2 = {'addr1': '555 nowhere', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
# data = {'name': 'bob', 'billing_address': address1, 'shipping_address': address2}
#
# json.dumps(marshal(data, resource_fields))
# '{"billing_address": {"line 1": "123 fake street", "line 2": null, "state": "NY", "zip": "10468", "city": "New York"},' \
# '"name": "bob",' \
# '"shipping_address": {"line 1": "555 nowhere", "line 2": null, "state": "NY", "zip": "10468", "city": "New York"}}'
