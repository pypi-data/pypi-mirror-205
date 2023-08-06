"""
Comment class
"""


import logging


LOGGER = logging.getLogger(__name__)


class Comment(object):
    """
    Used as a wrapper around individual sentences given in an ontology. Contains
    metrics on the sentence such as quantifier count, number of variables, type of
    predicates, etc. Also has utility methods to convert a sentence to FF-PCNF and
    potentially other formats.

    :param Logical sentence, a Logical object
    :return Axiom axiom
    """


    def __init__(self, text):

        self.text = text

    def __repr__(self):
        return self.text


    def ff_pcnf(self):
        """
        Apply logical operations to translate the axiom into a function free
        prenex conjunctive normal form.
        """

        return self.text

    def to_tptp(self):
        """
        Produce a TPTP representation of this comment.

        :return str tptp, TPTP formatted version of this axiom
        """

        # via http://tptp.cs.miami.edu/TPTP/QuickGuide/Problems.html
        # and https://tptp.org/NonClassicalLogic/SyntaxBNF.html

        return "% " + self.text


    def to_ladr(self):
        """
        Produce a LADR representation of this axiom.

        :return str ladr, LADR formatted version of this axiom
        """

        return "%\% " + self.text

    def to_latex(self):
        """
        Produce a LaTeX representation of this axiom.

        :return str latex, LaTeX formatted version of this axiom
        """

        return "% " + self.text


