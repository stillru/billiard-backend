import marshmallow as ma


class NewsSchema(ma.Schema):
    id = ma.fields.Integer()
    title = ma.fields.String()
    body = ma.fields.String()
    source_type = ma.fields.String()
    created_at = ma.fields.DateTime()
    tags = ma.fields.List(ma.fields.Integer())
