from sqlalchemy.orm import Session
from schemas import account_schema
from sql_app import models
import bcrypt


def create_account(database: Session, account: account_schema.UserSchema):
    if database.query(models.User).filter_by(username=account.username).first() is not None:
        return False
    database.add(
        models.User(
            username=account.username,
            password=bcrypt.hashpw(str.encode(account.password), bcrypt.gensalt(14)),
            fullname=account.fullname
        )
    )
    database.commit()
    return True
