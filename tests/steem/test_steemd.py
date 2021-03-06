from funcy.colls import pluck
from hive.hived import Hived


def test_get_version():
    """ We should be able to call get_version on hived """
    h = Hived()
    response = h.call('get_version', api='login_api')
    version = response['blockchain_version']
    assert version[0:4] == '0.20'


def test_get_dgp():
    """ We should be able to call get_dynamic_global_properties on hived """
    h = Hived()
    response = h.call('get_dynamic_global_properties', api='database_api')
    assert response['head_block_number'] > 20e6


def test_get_block():
    """ We should be able to fetch some blocks. """
    h = Hived()

    for num in [1000, 1000000, 10000000, 20000000, 21000000]:
        b = h.get_block(num)
        assert b, 'block %d was blank' % num
        assert num == int(b['block_id'][:8], base=16)

    start = 21000000
    for num in range(start, start + 50):
        b = h.get_block(num)
        assert b, 'block %d was blank' % num
        assert num == int(b['block_id'][:8], base=16)

    non_existent_block = 99999999
    b = h.get_block(non_existent_block)
    assert not b, 'block %d expected to be blank' % non_existent_block


def test_ensured_block_ranges():
    """ Post should load correctly if passed a dict or string identifier. """
    h = Hived()
    assert list(pluck('block_num', h.get_blocks_range(1000, 2000))) == list(
        range(1000, 2000))

    # for fuzzing in h.get_block_range_ensured() use:
    # degraded_results = [x for x in results if x['block_num'] %
    #     random.choice(range(1, 10)) != 0]
