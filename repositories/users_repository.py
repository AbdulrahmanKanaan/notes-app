from sqlalchemy.sql.expression import text
from models.user import User, UserCreate
from repositories.repository import Repository
from passlib.hash import bcrypt


class UsersRepository(Repository):

    def __init__(self) -> None:
        super().__init__()

    def getUserById(self, id: int) -> User:
        stmt = text(
            "SELECT * FROM users WHERE id=:id AND deleted_at IS NULL"
        )
        result = self.db.execute(stmt, id=id).fetchone()
        if (result):
            return User(**result)
        return None

    def getUserByEmail(self, email: str) -> User:
        stmt = text(
            "SELECT * FROM users WHERE email=:email AND deleted_at IS NULL"
        )
        result = self.db.execute(stmt, email=email).fetchone()
        if (result):
            return User(**result)
        return None

    def createUser(self, user: UserCreate) -> int:
        stmt = text(
            "INSERT INTO users(name, email, password, created_at, updated_at)" +
            "VALUES(:name, :email, :password, NOW(), NOW())"
        )
        result = self.db.execute(
            stmt, name=user.name, email=user.email,
            password=bcrypt.hash(user.password)
        )
        return result.lastrowid
