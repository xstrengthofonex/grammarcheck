from pos import TagAttemptResult, PosFacade


def test_gets_random_tagged_text():
    pos_facade = PosFacade()
    t1 = pos_facade.add_raw_text("This is a sentence")
    t2 = pos_facade.add_raw_text("This another sentence")
    t3 = pos_facade.add_raw_text("This is one more sentence")
    assert pos_facade.get_random_tagged_text() in [t1, t2, t3]


def test_successful_tag_attempt():
    pos_facade = PosFacade()
    text = pos_facade.add_raw_text("This is a sentence")
    result = pos_facade.make_tag_attempt(text.id, [
        ("This", "DT"), ("is", "VBZ"), ("a", "DT"), ("sentence", "NN")])
    assert result == TagAttemptResult(100, [
        ("This", True),
        ("is", True),
        ("a", True),
        ("sentence", True)])


def test_failed_tag_attempt():
    pos_facade = PosFacade()
    text = pos_facade.add_raw_text("This is a sentence")
    result = pos_facade.make_tag_attempt(text.id, [
        ("This", "DT"), ("is", "NN"), ("a", "PRP"), ("sentence", "NN")])
    assert result == TagAttemptResult(50, [
        ("This", True),
        ("is", False),
        ("a", False),
        ("sentence", True)])
