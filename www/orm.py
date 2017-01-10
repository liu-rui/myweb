class ModelMetaclass(type):
    __KEY_FIELDS = '_fields'
    __KEY_TABLE__NAME = '_table_name'

    def __new__(cls, name, bases, attrs):
        if name != 'Model':
            ModelMetaclass._refactor(name, attrs)
        return type.__new__(cls, name, bases, attrs)

    @staticmethod
    def _refactor(name, attrs):
        ModelMetaclass. _refactor_table_name(name, attrs)
        ModelMetaclass._refactor_fields(attrs)

    @staticmethod
    def _refactor_table_name(name,  attrs):
        table_name = attrs.get('__table__', None)

        if table_name is None:
            attrs[ModelMetaclass.__KEY_TABLE__NAME] = name
        else:
            attrs[ModelMetaclass.__KEY_TABLE__NAME] = table_name
            attrs.pop('__table__')

    @staticmethod
    def _refactor_fields(attrs):
        fields = list()

        for k, v in attrs.items():
            if isinstance(v,  Field):
                v.attr_name = k
                fields.append(v)

        fields.sort(key=lambda x: x.column_name)
        attrs[ModelMetaclass.__KEY_FIELDS] = fields

        for k in fields:
            attrs.pop(k.attr_name)

    @staticmethod
    def _generateSql(attrs):
        table_name = attrs[ModelMetaclass.__KEY_TABLE__NAME]
        fields = attrs[ModelMetaclass.__KEY_FIELDS]
        attrs["_insert"] = 'insert into %s (%s) values(%s)' % (
            table_name, ','.join((x.column_name for x in fields)),  ',' .join('?' * len(fields)))


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self[name] = value

    @classmethod
    def add(cls, model):
        return getattr(cls, "_insert")


class Field(object):

    def __init__(self, name, column_type, primary_key):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key

    @property
    def attr_name(self):
        return self.__attr_name

    @attr_name.setter
    def attr_name(self, value):
        self.__attr_name = value

    @property
    def column_name(self):
        return self.name if self.name is not None else self.__attr_name

    def __str__(self):
        return '%s >> %s %s' % (self.name, self.column_name, self.column_type)

    __repr__ = __str__


class Integer(Field):

    def __init__(self, name=None, primary_key=None):
        super(Integer, self).__init__(name,  'int', primary_key)


class String(Field):

    def __init__(self, name=None, len=100, primary_key=None):
        super(String, self).__init__(name,  'varchar(%d)' % len, primary_key)
