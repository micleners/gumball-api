"""
Model classes for OpsHub DB objects
"""
import sqlalchemy as sa
from sqlalchemy.ext import declarative
from sqlalchemy import orm

Base = declarative.declarative_base()


class GumballMachine(Base):
    __tablename__ = 'gumball_machine'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    serial_no = sa.Column(sa.String(5), unique=True, nullable=False, index=True)

    transactions = orm.relationship('GumballTransaction', back_populates='machine')


class GumballTransaction(Base):
    __tablename__ = 'gumball_transaction'

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    trans_id = sa.Column(sa.BigInteger, nullable=False)

    serial_no = sa.Column(sa.String(5),
                          sa.ForeignKey('gumball_machine.serial_no'),
                          nullable=False)
    trans_date = sa.Column(sa.DateTime, nullable=False)
    dispense_count = sa.Column(sa.SmallInteger, nullable=False)

    _uix_trans_id__serial_no = sa.UniqueConstraint(trans_id, serial_no,
                                                   name='uix_gumball_transaction__trans_id__serial_no')

    machine = orm.relationship('GumballMachine', back_populates='transactions')
