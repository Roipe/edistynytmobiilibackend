import os
from typing import List, Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Index, Integer, String, Text, create_engine, Table, \
    ForeignKey
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship, sessionmaker, Session
from sqlalchemy.orm.base import Mapped

load_dotenv()

engine = create_engine(os.getenv('DB'))
ses = sessionmaker(bind=engine)

Base = declarative_base()
metadata = Base.metadata

from typing import List

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class AuthRole(Base):
    __tablename__ = 'auth_role'
    __table_args__ = (
        Index('role_name_UNIQUE', 'role_name', unique=True),
    )

    auth_role_id = mapped_column(Integer, primary_key=True)
    role_name = mapped_column(String(45), nullable=False)

    auth_user: Mapped[List['AuthUser']] = relationship('AuthUser', uselist=True, back_populates='auth_role_auth_role')


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (
        Index('category_name_UNIQUE', 'category_name', unique=True),
    )

    category_id = mapped_column(Integer, primary_key=True)
    category_name = mapped_column(String(45), nullable=False)

    rental_item: Mapped[List['RentalItem']] = relationship('RentalItem', uselist=True,
                                                           back_populates='category_category')


class RentalItemFeature(Base):
    __tablename__ = 'rental_item_feature'

    rental_item_feature_id = mapped_column(Integer, primary_key=True)
    rental_item_feature_name = mapped_column(String(45), nullable=False)

    rental_item_has_rental_item_feature: Mapped[List['RentalItemHasRentalItemFeature']] = relationship(
        'RentalItemHasRentalItemFeature', uselist=True, back_populates='rental_item_feature_rental_item_feature')


class RentalItemState(Base):
    __tablename__ = 'rental_item_state'
    __table_args__ = (
        Index('rental_item_state_UNIQUE', 'rental_item_state', unique=True),
    )

    rental_item_state_id = mapped_column(Integer, primary_key=True)
    rental_item_state = mapped_column(String(45), nullable=False)

    rental_item: Mapped[List['RentalItem']] = relationship('RentalItem', uselist=True,
                                                           back_populates='rental_item_state_rental_item_state')


class RentalTransactionState(Base):
    __tablename__ = 'rental_transaction_state'
    __table_args__ = (
        Index('rental_transaction_state_UNIQUE', 'rental_transaction_state', unique=True),
    )

    rental_transaction_state_id = mapped_column(Integer, primary_key=True)
    rental_transaction_state = mapped_column(String(45), nullable=False)

    rental_transaction: Mapped[List['RentalTransaction']] = relationship('RentalTransaction', uselist=True,
                                                                         back_populates='rental_transaction_state_rental_transaction_state')


class AuthUser(Base):
    __tablename__ = 'auth_user'
    __table_args__ = (
        ForeignKeyConstraint(['auth_role_auth_role_id'], ['auth_role.auth_role_id'], name='fk_auth_user_auth_role'),
        Index('fk_auth_user_auth_role_idx', 'auth_role_auth_role_id'),
        Index('username_UNIQUE', 'username', unique=True)
    )

    auth_user_id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(45), nullable=False)
    password = mapped_column(String(255), nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    auth_role_auth_role_id = mapped_column(Integer, nullable=False)
    deleted_at = mapped_column(DateTime)
    access_jti = mapped_column(String(255))

    auth_role_auth_role: Mapped['AuthRole'] = relationship('AuthRole', back_populates='auth_user')
    rental_item: Mapped[List['RentalItem']] = relationship('RentalItem', uselist=True, back_populates='created_by_user')
    rental_transaction: Mapped[List['RentalTransaction']] = relationship('RentalTransaction', uselist=True,
                                                                         back_populates='auth_user_auth_user')


class RentalItem(Base):
    __tablename__ = 'rental_item'
    __table_args__ = (
        #Index('serial_number_unique', 'serial_number', unique=True),
        ForeignKeyConstraint(['category_category_id'], ['category.category_id'], name='fk_rental_item_category1'),
        ForeignKeyConstraint(['created_by_user_id'], ['auth_user.auth_user_id'], name='fk_rental_item_auth_user1'),
        ForeignKeyConstraint(['rental_item_state_rental_item_state_id'], ['rental_item_state.rental_item_state_id'],
                             name='fk_rental_item_rental_item_state1'),
        Index('fk_rental_item_auth_user1_idx', 'created_by_user_id'),
        Index('fk_rental_item_category1_idx', 'category_category_id'),
        Index('fk_rental_item_rental_item_state1_idx', 'rental_item_state_rental_item_state_id')

    )

    rental_item_id = mapped_column(Integer, primary_key=True)
    rental_item_name = mapped_column(String(45), nullable=False)
    created_at = mapped_column(DateTime, nullable=False)
    created_by_user_id = mapped_column(Integer, nullable=False)
    rental_item_state_rental_item_state_id = mapped_column(Integer, nullable=False)
    category_category_id = mapped_column(Integer, nullable=False)
    # rental_item_description = mapped_column(Text)
    # serial_number = mapped_column(String(45), nullable=False)
    deleted_at = mapped_column(DateTime)

    category_category: Mapped['Category'] = relationship('Category', back_populates='rental_item')
    created_by_user: Mapped['AuthUser'] = relationship('AuthUser', back_populates='rental_item')
    rental_item_state_rental_item_state: Mapped['RentalItemState'] = relationship('RentalItemState',
                                                                                  back_populates='rental_item')

    rental_item_has_rental_item_feature: Mapped[List['RentalItemHasRentalItemFeature']] = relationship(
        'RentalItemHasRentalItemFeature', uselist=True, back_populates='rental_item_rental_item')

    rental_transaction: Mapped[List['RentalTransaction']] = relationship('RentalTransaction', uselist=True,
                                                                         back_populates='rental_item_rental_item')


class RentalItemHasRentalItemFeature(Base):
    __tablename__ = 'rental_item_has_rental_item_feature'
    __table_args__ = (
        ForeignKeyConstraint(['rental_item_feature_rental_item_feature_id'],
                             ['rental_item_feature.rental_item_feature_id'],
                             name='fk_rental_item_has_rental_item_feature_rental_item_feature1'),
        ForeignKeyConstraint(['rental_item_rental_item_id'], ['rental_item.rental_item_id'],
                             name='fk_rental_item_has_rental_item_feature_rental_item1'),
        Index('fk_rental_item_has_rental_item_feature_rental_item1_idx', 'rental_item_rental_item_id'),
        Index('fk_rental_item_has_rental_item_feature_rental_item_feature1_idx',
              'rental_item_feature_rental_item_feature_id')
    )

    rental_item_rental_item_id = mapped_column(Integer, primary_key=True, nullable=False)
    rental_item_feature_rental_item_feature_id = mapped_column(Integer, primary_key=True, nullable=False)
    value = mapped_column(String(45), nullable=False)

    # tama
    rental_item_feature_rental_item_feature: Mapped['RentalItemFeature'] = relationship('RentalItemFeature',
                                                                                        back_populates='rental_item_has_rental_item_feature')
    rental_item_rental_item: Mapped['RentalItem'] = relationship('RentalItem',
                                                                 back_populates='rental_item_has_rental_item_feature')


class RentalTransaction(Base):
    __tablename__ = 'rental_transaction'
    __table_args__ = (
        ForeignKeyConstraint(['auth_user_auth_user_id'], ['auth_user.auth_user_id'],
                             name='fk_rental_transaction_auth_user1'),
        ForeignKeyConstraint(['rental_item_rental_item_id'], ['rental_item.rental_item_id'],
                             name='fk_rental_transaction_rental_item1'),
        ForeignKeyConstraint(['rental_transaction_state_rental_transaction_state_id'],
                             ['rental_transaction_state.rental_transaction_state_id'],
                             name='fk_rental_transaction_rental_transaction_state1'),
        Index('fk_rental_transaction_auth_user1_idx', 'auth_user_auth_user_id'),
        Index('fk_rental_transaction_rental_item1_idx', 'rental_item_rental_item_id'),
        Index('fk_rental_transaction_rental_transaction_state1_idx',
              'rental_transaction_state_rental_transaction_state_id')
    )

    rental_transaction_id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime, nullable=False)
    rental_item_rental_item_id = mapped_column(Integer, nullable=False)
    auth_user_auth_user_id = mapped_column(Integer, nullable=False)
    rental_transaction_state_rental_transaction_state_id = mapped_column(Integer, nullable=False)

    auth_user_auth_user: Mapped['AuthUser'] = relationship('AuthUser', back_populates='rental_transaction')
    rental_item_rental_item: Mapped['RentalItem'] = relationship('RentalItem', back_populates='rental_transaction')
    rental_transaction_state_rental_transaction_state: Mapped['RentalTransactionState'] = relationship(
        'RentalTransactionState', back_populates='rental_transaction')


def get_db():
    db = ses()
    try:

        yield db

    finally:

        db.close()


Db = Annotated[Session, Depends(get_db)]
