from models.user import User


def test_user_query(db, users):
    """Test querying users from the database."""
    # query_executed_directly = User.query.filter_by(email="john@mail.com").first()

    """ Test querying users from the database using the query object."""
    query = db.select(User).where(User.email == "john@mail.com").limit(1)
    """ Hasil query di atas adalah:
        SELECT users.id, users.username, users.email, users.password, users.created_at, users.updated_at, users.last_login, users.is_active, users.is_admin 
        FROM users 
        WHERE users.email = :email_1
        LIMIT :param_1
    """

    # user = db.session.execute(query).scalars().first()  # or
    user = db.session.execute(query).scalar_one()
    print(user)
    assert user.username == "john"
