import unittest
import www.orm as orm
import logging


class OrmTest(unittest.TestCase):

    def test_1(self):

        class User(orm.Model):
            pass

        user = User(id=10, name='ren')
        self.assertIsNotNone(user)
        self.assertEqual(10, user.id)
        self.assertEqual('ren', user.name)

    def test_2(self):
        class User(orm.Model):
            __table__ = 'User'

        class Customer(orm.Model):
            pass

        self.assertEqual('User', User._table_name)
        self.assertEqual('Customer', Customer._table_name)

    def test_3(self):
        class User(orm.Model):
            __table__ = 'User'

            id1 = orm.Integer()
            id2 = orm.Integer('id')
            id3 = orm.Integer(primary_key=True)

        fields = User._fields
        self.assertIsNotNone(fields)
        self.assertEqual(3, len(fields))
        id1Field = next(filter(lambda x: x.attr_name == 'id1', fields))
        self.assertEqual('id1',  id1Field.column_name)
        self.assertIsNone(id1Field.primary_key)

        id2Field = next(filter(lambda x: x.attr_name == 'id2', fields))
        self.assertEqual('id',  id2Field.column_name)
        self.assertIsNone(id2Field.primary_key)

        id3Field = next(filter(lambda x: x.attr_name == 'id3', fields))
        self.assertEqual('id3',  id3Field.column_name)
        self.assertTrue(id3Field.primary_key)

    def test_4(self):
        class User(orm.Model):
            __table__ = 'User'
            id1 = orm.Integer()

        user = User(id1=23)
        self.assertEqual('insert into User (id1) values(23)', User.add(user))
