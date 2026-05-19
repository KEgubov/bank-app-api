import datetime
import enum
from typing import Optional, Annotated

from sqlalchemy import (
    ForeignKey,
    Numeric,
    text,
    String,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

str_3 = Annotated[str, 3]
str_5 = Annotated[str, 5]
str_12 = Annotated[str, 12]
str_20 = Annotated[str, 20]
str_16 = Annotated[str, 16]
str_45 = Annotated[str, 45]
str_50 = Annotated[str, 50]
str_100 = Annotated[str, 100]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_3: String(3),
        str_5: String(5),
        str_12: String(12),
        str_16: String(16),
        str_20: String(20),
        str_45: String(45),
        str_50: String(50),
        str_100: String(100),
    }

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)!r}")
        return f"<{self.__class__.__name__}, {', '.join(cols)}>"


class User(Base):
    """
    Модель пользователя в базе данных.
    __tablename__ = "user"
    __table_args__ = UniqueConstraint("login", "password", name="uq_login_password") -
    составной индекс из логина и пароля
    Имеет 2 relationships, contacts и account.
    У одного пользователя может быть много контактов и счетов (one to many связь)
    """

    __tablename__ = "user"

    user_id: Mapped[intpk]
    first_name: Mapped[Optional[str_50]]
    last_name: Mapped[Optional[str_50]]
    super_last_name: Mapped[Optional[str_50]]
    phone_number: Mapped[str_12] = mapped_column(unique=True)
    password: Mapped[str_20]
    email: Mapped[Optional[str_45]] = mapped_column(unique=True)

    contact: Mapped[list["Contact"]] = relationship(
        back_populates="user",
    )
    account: Mapped["Account"] = relationship(
        back_populates="user",
    )
    card: Mapped["Card"] = relationship(
        back_populates="user",
    )


class Contact(Base):
    """
    Модель контакта в базе данных.
    __tablename__ = "contact"
    ForeignKey - User.user_id, каскадное удаление
    Имеет 1 relationship, user.
    У множества контактов может быть только один пользователь (many to one relationship)
    """

    __tablename__ = "contact"

    contact_id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"))
    first_name: Mapped[Optional[str_50]]
    last_name: Mapped[Optional[str_50]]
    super_last_name: Mapped[Optional[str_50]]
    phone_number: Mapped[Optional[str_12]] = mapped_column(unique=True)

    user: Mapped["User"] = relationship(
        back_populates="contact",
    )

    __table_args__ = (Index("idx_contact_user_id", "user_id"),)


class Account(Base):
    """
    Модель счёта в базе данных.
    __tablename__ = "account"
    __table_args__ = CheckConstraint("balance >= 0", name="balance_check") -
    Ограничение уровня таблицы, которое проверяет валидность баланса.
    ForeignKey - User.user_id, каскадное удаление, уникальный индекс
    Имеет 3 relationships, user, card, transaction.
    У одного счёта может быть только 1 пользователь (one to one relationship),
    У одного счёта может быть множество карт (one to many relationship),
    У одного счёта может быть множество операций (one to many relationship)
    """

    __tablename__ = "account"

    account_id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"), unique=True
    )
    account_number: Mapped[str_20] = mapped_column(unique=True)
    balance: Mapped[Numeric] = mapped_column(Numeric(15, 2), default=0.00)
    total_operations: Mapped[int] = mapped_column(default=0)
    last_activity_date: Mapped[Optional[datetime.datetime]]

    user: Mapped["User"] = relationship(
        back_populates="account",
    )
    card: Mapped[list["Card"]] = relationship(
        back_populates="account",
    )
    transaction: Mapped[list["Transaction"]] = relationship(
        back_populates="account",
    )

    __table_args__ = (
        CheckConstraint("balance >= 0", name="balance_check"),
        Index("idx_account_user_id", "user_id"),
    )


class Card(Base):
    """
    Модель карты в базе данных.
    __tablename__ = "card"
    ForeignKey - Account.account_id
    ForeignKey = User.phone_number
    Имеет 1 relationship, account.
    У множества карт может быть только 1 счёт (many to one relationship).
    """

    __tablename__ = "card"

    card_number: Mapped[str_16] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"))
    phone_number: Mapped[Optional[str_12]] = mapped_column(ForeignKey("user.phone_number"))
    card_holder_name: Mapped[Optional[str_100]]
    valid_through_date: Mapped[Optional[str_5]]
    cvv2_cvc2_number: Mapped[Optional[str_3]]

    account: Mapped["Account"] = relationship(
        back_populates="card",
    )
    user: Mapped["User"] = relationship(
        back_populates="card",
    )

    __table_args__ = (
        Index("idx_card_account_id", "account_id"),
        Index("idx_card_phone_number", "phone_number"),
    )


class TxnType(enum.Enum):
    """
    Тип данных Enum используемый в табличной моделе transaction для атрибута
    txn_type.
    """

    C = "C"
    D = "D"


class Transaction(Base):
    """
    Модель транзакции для базы данных.
    __tablename__ = "transaction"
    ForeignKey - Account.account_id, каскадное удаление, уникальный индекс.
    Имеет 1 relationship, account.
    У множества транзакций может быть 1 счёт (many to one relationship).
    """

    __tablename__ = "transaction"

    txn_id: Mapped[intpk]
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.account_id", ondelete="CASCADE")
    )
    card_number: Mapped[Optional[str_16]]
    txn_type: Mapped[Optional[TxnType]]
    amount: Mapped[Numeric] = mapped_column(Numeric(15, 2))
    txn_date: Mapped[Optional[datetime.datetime]] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    account: Mapped["Account"] = relationship(
        back_populates="transaction",
    )

    __table_args__ = (Index("idx_txn_account_id", "account_id"),)
