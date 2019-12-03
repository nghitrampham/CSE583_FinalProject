'''
test the output of the correlation data
'''

import correlation_county_test

def test_correlation_county_test():
    cor, year, county, state = throu_the_country()
    length = len(cor)
    assert len(year) == length
    assert len(county) == length
    assert len(state) == length

    for i in cor:
        assert type(cor[i]) is float
        assert type(year[i]) is int
        assert type(county[i]) is int
        assert type(state[i]) is int