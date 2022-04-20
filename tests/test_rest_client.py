import datetime

from taosrest.restclient import RestClient


def test_auth():
    client = RestClient("localhost", 6041, "root", "taosdata")
    print(client.token)


def test_show_database():
    client = RestClient("localhost", 6041, "root", "taosdata")
    resp = client.sql("show databases")
    print("\n", resp)
    # {'status': 'succ', 'head': ['name', 'created_time', 'ntables', 'vgroups', 'replica', 'quorum', 'days', 'keep', 'cache(MB)', 'blocks', 'minrows', 'maxrows', 'wallevel', 'fsync', 'comp', 'cachelast', 'precision', 'update', 'status'], 'column_meta': [['name', 8, 32], ['created_time', 9, 8], ['ntables', 4, 4], ['vgroups', 4, 4], ['replica', 3, 2], ['quorum', 3, 2], ['days', 3, 2], ['keep', 8, 24], ['cache(MB)', 4, 4], ['blocks', 4, 4], ['minrows', 4, 4], ['maxrows', 4, 4], ['wallevel', 2, 1], ['fsync', 4, 4], ['comp', 2, 1], ['cachelast', 2, 1], ['precision', 8, 3], ['update', 2, 1], ['status', 8, 10]], 'data': [['test', '2022-04-07T13:15:26.857+08:00', 8, 1, 1, 1, 10, '3650', 16, 6, 100, 4096, 1, 3000, 2, 0, 'ms', 0, 'ready'], ['log', '2022-03-26T15:54:26.997+08:00', 150, 1, 1, 1, 10, '30', 1, 3, 100, 4096, 1, 3000, 2, 0, 'us', 0, 'ready'], ['power', '2022-04-14T14:44:00.059+08:00', 4, 1, 1, 1, 10, '3650', 16, 6, 100, 4096, 1, 3000, 2, 0, 'ms', 0, 'ready']], 'rows': 3}


def test_insert_data():
    c = RestClient("localhost", 6041, "root", "taosdata")
    c.sql("drop database if exists test")
    c.sql("create database test")
    c.sql("create table test.tb2 (ts timestamp, c1 int, c2 double, c3 timestamp)")
    resp = c.sql("insert into test.tb2 values (now, -100, -200.3, now+1m) (now+10s, -101, -340.2423424, now+2m)")
    print("\n==============insert resp==============")
    print(resp)
    assert resp["rows"] == 1


def test_describe_table():
    c = RestClient("localhost", 6041, "root", "taosdata")
    try:
        c.sql("describe test.noexits")
        assert False
    except:
        pass


def test_select_data_with_timestamp_type():
    c = RestClient("localhost", 6041, "root", "taosdata")
    resp = c.sql("select * from test.tb2")
    data = resp["data"]
    assert isinstance(data[0][0], datetime.datetime)
    assert isinstance(data[0][3], datetime.datetime)
