from sqlalchemy.orm import Session
from schemas import account_schema
from sql_app import models


def create_account(database: Session, account: account_schema.UserSchema):
    if database.query(models.Users).filter_by(username=account.username).first() is not None:
        return False
    database.add(
        models.Users(
            username=account.username,
            password=account.password,
            fullname=account.fullname
        )
    )
    database.commit()
    return True
