from corpus import MEMORIES


def test_corpus_has_fifty_memories():
    assert len(MEMORIES) == 50


def test_corpus_query_targets_present():
    contents = [m["content"] for m in MEMORIES]
    assert any("Prefers Python for anything ML" in c for c in contents)
    assert any("Reports to Priya Menon" in c for c in contents)
    assert any("latency regression in the research pipeline" in c for c in contents)
    assert any("p99 is 840 ms" in c for c in contents)


def test_every_memory_has_content_and_tags():
    for m in MEMORIES:
        assert isinstance(m["content"], str) and m["content"]
        assert isinstance(m["tags"], list)
        assert m["tags"]
