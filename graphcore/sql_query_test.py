import pytest

from .sql_query import SQLQuery, mysql_col


def test_simple_query_merge():
    book_id = SQLQuery(['users', 'books'], 'books.id', {
        'users.id': 1,
        'books.user_id': mysql_col('user.id'),
    })

    combined = SQLQuery(['books'], 'books.name', {
        'books.id': book_id
    })

    assert combined == SQLQuery(
        'users, books', 'books.name', {
            'users.id': 1,
            'books.user_id': mysql_col('user.id'),
        })

def test_simple_add():
    first_name = SQLQuery(['users'], 'users.first_name', {
        'users.id': 1,
    })
    last_name = SQLQuery(['users'], 'users.last_name', {
        'users.id': 1,
    })

    first_and_last_name = SQLQuery(
        ['users'], ['users.first_name', 'users.last_name'], {
            'users.id': 1,
        }
    )

    assert first_name + last_name == first_and_last_name

def test_hash():
    def build():
        SQLQuery(['users'], 'users.first_name', {
            'users.id': 1,
        }, {
            'users.name': 'name',
        })

    assert hash(build()) == hash(build())


def test_assert_flattenable_table_alias():
    with pytest.raises(ValueError):
        SQLQuery(['users u'], 'users.id', {})


def test_assert_flattenable_column_with_no_table():
    with pytest.raises(ValueError):
        SQLQuery(['users'], 'id', {})


def test_assert_flattenable_clause_with_no_table():
    with pytest.raises(ValueError):
        SQLQuery(['users'], 'users.id', {'id': 1})
