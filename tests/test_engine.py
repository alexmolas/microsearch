from microsearch.engine import SearchEngine


def test_search_engine():
    engine = SearchEngine()
    docs = [("foo", "foo content"), ("bar", "bar content")]
    engine.bulk_index(docs)
    
    assert engine.search("content")["foo"] == engine.search("content")["bar"]
    assert len(engine.search("foo")) == 1
    assert len(engine.search("bar")) == 1
