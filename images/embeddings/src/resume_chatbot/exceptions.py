class ResumeEmbeddingError(Exception):
    def __init__(self, msg="Error while embedding resumes."):
        super().__init__(msg)
