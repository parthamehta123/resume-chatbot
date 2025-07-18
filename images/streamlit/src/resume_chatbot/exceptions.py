class NoResultsError(Exception):
    def __init__(self, msg="No matching resumes found."):
        super().__init__(msg)
