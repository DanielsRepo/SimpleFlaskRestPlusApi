import requests

from app import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True, nullable=False)

    @staticmethod
    def create_user(data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user(user_id):
        return User.query.get_or_404(user_id)

    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()


# ETL script
@db.event.listens_for(User.__table__, "after_create")
def load_users(*args, **kwargs):
    print("Starting ETL script...")

    gender = "male"
    quan = 100

    response = requests.get(
        f"https://randomuser.me/api/?gender={gender}&results={quan}"
    )

    for user in response.json()["results"]:
        db.session.add(
            User(
                firstname=user["name"].get("first"),
                lastname=user["name"].get("last"),
                gender=user.get("gender"),
                email=user.get("email"),
                phone=user.get("phone"),
            )
        )

    db.session.commit()

    print("100 random users with male gender have been loaded")
