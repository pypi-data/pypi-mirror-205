from simplechain.stack.text_embedders.base import TextEmbedder
from simplechain.stack.text_generators.base import TextGenerator
from simplechain.stack.vector_databases.base import VectorDatabase


class TextEmbedderFactory:
    @classmethod
    def create(cls, name: str, **kwargs) -> TextEmbedder:
        if name == "openai":
            from simplechain.stack.text_embedders.openai import TextEmbedderOpenAI
            return TextEmbedderOpenAI(**kwargs)
        elif name == "ai21":
            from simplechain.stack.text_embedders.ai21 import TextEmbedderAI21
            return TextEmbedderAI21(**kwargs)
        else:
            raise ValueError(f"Invalid name: {name}.")

    @classmethod
    def createOpenAI(cls, **kwargs) -> TextEmbedder:
        from simplechain.stack.text_embedders.openai import TextEmbedderOpenAI
        return TextEmbedderOpenAI(**kwargs)


class VectorDatabaseFactory:
    @classmethod
    def create(cls, name: str, *args, **kwargs) -> VectorDatabase:
        if name == "annoy":
            from simplechain.stack.vector_databases.annoy import Annoy
            return Annoy(*args, **kwargs)
        else:
            raise ValueError(f"Invalid name: {name}.")


class PDFLoaderFactory:
    import langchain

    @classmethod
    def create(cls, name: str, file_path: str) -> langchain.document_loaders.pdf.BasePDFLoader:
        if name == "unstructured":
            from langchain.document_loaders import UnstructuredPDFLoader
            loader = UnstructuredPDFLoader(file_path)
            data = loader.load()
        elif name == "pdfminer":
            from langchain.document_loaders import PDFMinerLoader
            loader = PDFMinerLoader(file_path)
            data = loader.load()
        elif name == "pypdf":
            from langchain.document_loaders import PyPDFLoader
            loader = PyPDFLoader(file_path)
            data = loader.load_and_split()
        elif name == "onlinepdf":
            from langchain.document_loaders import OnlinePDFLoader
            loader = OnlinePDFLoader(file_path)
            data = loader.load()
        elif name == "pymupdf":
            from langchain.document_loaders import PyMuPDFLoader
            loader = PyMuPDFLoader(file_path)
            data = loader.load()
        else:
            raise ValueError(f"Invalid name: {name}.")
        return data


class TextGeneratorFactory:
    @classmethod
    def create(cls, name: str, **kwargs) -> TextGenerator:
        if name == "openai":
            from simplechain.stack.text_generators.llms.openai import TextGeneratorOpenAI
            return TextGeneratorOpenAI(**kwargs)
        elif name == "ai21":
            from simplechain.stack.text_generators.llms.ai21 import TextGeneratorAI21
            return TextGeneratorAI21(**kwargs)
        else:
            raise ValueError(f"Invalid name: {name}.")
