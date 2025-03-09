from app.dao.base import BaseDAO
from app.models import User


class UsersDAO(BaseDAO):
    model = User


