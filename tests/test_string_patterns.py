from slash.utils.pattern_matching import Matcher


def test_string_patterns(populated_suite, config_override):
    selected_test = populated_suite[len(populated_suite) // 2]

    config_override("run.filter_string", selected_test.uuid)

    for i, test in enumerate(populated_suite):
        if test is not selected_test:
            test.expect_deselect()

    populated_suite.run()


def test_matcher():
    for pattern, matching, not_matching in [
            ('xy', ['blapxy'], ['blap']),
            ('not x', ['blap', 'yyy'], ['blapx', 'xy']),
            ('x and y', ['xy', 'yx', 'x kjfldkjfd y'], ['x', 'y', 'xx']),
            ('(x and some.string) and not z', ['xysome.string', 'some.stringyx'], ['z', 'xysome.stringz']),
            ('exact(x=y)(y=z)', ['exact(x=y)(y=z)'], ['exlact(x=y)(y=z)']),
            ]:

        matcher = Matcher(pattern)
        for string in matching:
            assert matcher.matches(string)
        for string in not_matching:
            assert not matcher.matches(string)
