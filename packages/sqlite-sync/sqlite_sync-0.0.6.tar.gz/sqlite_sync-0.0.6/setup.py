from setuptools import setup

setup(
    name='sqlite_sync',
    version='0.0.6',
    description='SQLite3 wrapper for query synchronization',
    long_description='''SQLite3 is a lightweight embeddable database that is widely used in various projects. However, using SQLite3 multithreaded can lead to unexpected results such as data loss, blocking, recursive errors.

Our library solves this problem by providing a solution for SQLite3 multithreading. We provide an improved interface that allows database relationships to be used from different connections, thus avoiding locking the database and ensuring data integrity.

The library provides a simple and clear API that allows you to quickly and easily create and manipulate various UDP socket connections.

Our features, such as SQLite3 concurrency, great performance, and a simple API, allow developers to interact with their database more conveniently and quickly. Our goal is to help developers build efficient and stable systems using SQLite3.''',
    author='Robert Popov',
    author_email='robert@berht.dev',
    url='https://github.com/RobertMeow/sqlite_sync',

    packages=['sqlite_sync']
)
