import logging
import os
from pathlib import PureWindowsPath, PurePosixPath
from typing import Dict, Optional

from docx import Document
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader, BaseLoader


class WordGenerator:
    """
    A class that reads a docx template, where you can inject, like a Jinja2 template, some variables.
    """

    def __init__(self, docx_template: str, begin_separator: str = "<<", end_separator: str = ">>"):
        """
        Create a new docx template based on the docx
        :param docx_template:
        """
        self.docx_template = docx_template
        self.begin_separator = begin_separator
        self.end_separator = end_separator

    def create_instance_of(self, docx: str, vars: Dict[str, any], loader: Optional[BaseLoader] = None) -> str:
        """
        Generate a new file representing the docx instantiation

        :param docx: name of the file to generate. If it is a relative path, it is relative to "."
        :param vars: set of variables and functions you can use inside the docx variable parameters.
        :param loader: the loader to use to load templates. If missing, we will use `FileSystemLoader("../templates")`
        :return:
        """
        if loader is None:
            loader = FileSystemLoader(searchpath="./")
        env = Environment(
            loader=loader,
            autoescape=select_autoescape(),
            lstrip_blocks=True,
            newline_sequence="\r\n",
            variable_start_string=self.begin_separator,
            variable_end_string=self.end_separator,
        )

        # generates new template file instance. By documentation, we need to use "/" as separator, even on windows
        p = PureWindowsPath(self.docx_template).as_posix()
        logging.info(f"loading template in {p}")
        template = env.get_template(p)
        document = Document(docx)
        # outputText = template.render()  # this is where to put args to the template renderer

        for paragraph in document.paragraphs:
            print(paragraph.text)

        template.stream(vars).dump(docx)
        return docx
