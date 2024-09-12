from dataclasses import dataclass

import pytest


@dataclass
class FakeUserRepository:
    ... # аналог pass



@pytest.fixture
def user_repository():
    return FakeUserRepository()