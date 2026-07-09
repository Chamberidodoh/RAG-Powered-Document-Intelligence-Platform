class RAGException(Exception):
    """Base exception for the application."""


class UnsupportedFileTypeError(RAGException):
    pass


class FileTooLargeError(RAGException):
    pass


class EmptyDocumentError(RAGException):
    pass


class DocumentNotFoundError(RAGException):
    pass


class DocumentProcessingError(RAGException):
    pass


class EmbeddingGenerationError(RAGException):
    pass


class VectorDatabaseError(RAGException):
    pass


class RetrievalError(RAGException):
    pass


class OpenAIAPIError(RAGException):
    pass


class InvalidQuestionError(RAGException):
    pass
