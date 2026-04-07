from app.users.dao import UsersDAO

import pytest

@pytest.mark.parametrize("user_id,email,exists", [
    (1, "matthew.ss0089@gmail.com", True),
    (2, "reboy@kpi.ua", True),
    (52, "...", False)
])
async def test_find_user_by_id(user_id, email, exists):
    user = await UsersDAO.find_by_id(user_id)
    
    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user