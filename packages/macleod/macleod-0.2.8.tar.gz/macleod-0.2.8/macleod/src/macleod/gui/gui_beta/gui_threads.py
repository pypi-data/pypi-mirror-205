from PyQt5.QtCore import QThread
from macleod.parsing import parser as Parser
import os
import macleod.Filemgt as filemgt
import tempfile
import sys
import traceback


class ParseThread(QThread):
    """
    Runs the parser and returns an ontology object
    """

    def __init__(self):
        QThread.__init__(self)

        # input
        self.resolve = False
        self.text = None
        self.path = None

        # output
        self.error = ErrorBuffer()
        self.ontology = None

    def __del__(self):
        self.wait()

    def run(self):
        # We need to capture the print statements from the parser
        backup = sys.stdout
        sys.stdout = self.error

        # Create a place to read the text from
        buffer = tempfile.mkstemp(".macleod")
        with open(buffer[1], 'w') as f:
            f.write(self.text)

        try:
            self.ontology = Parser.parse_file(buffer[1],
                                              filemgt.read_config('cl', 'prefix'),
                                              os.path.abspath(filemgt.read_config('system', 'path')),
                                              self.resolve,
                                              self.path)

        except Exception as e:
            print(e)
            # If it's not a CL error we need to find the problem in Python
            if not isinstance(e, TypeError):
                # This prints to the Python console, not to the console in the window
                traceback.print_exc()
            self.ontology = None

        # return to the previous output
        sys.stdout = backup

        # leave no trace of the buffer
        os.close(buffer[0])
        os.remove(buffer[1])


class ErrorBuffer:
    """
    A place to capture errors
    """

    def __init__(self):
        self.contents = ""

    def write(self, text):
        self.contents += text

    def flush(self):
        self.contents = ""
