# Since python 2.7 doesn't support enums,
class BulbStates:
    def __init__(self):
        pass

    OFF, NOT_HOME, NOT_AROUND, IN_BED, NOT_WASTED = range(5)