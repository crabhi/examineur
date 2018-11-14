##
# The tested notebook will be available as module `tested_nb`
#
import tested_nb


def test_exercise_01():
    assert tested_nb.return_one() == 1


def test_exercise_02():
    assert tested_nb.sqrt(9) == 3
