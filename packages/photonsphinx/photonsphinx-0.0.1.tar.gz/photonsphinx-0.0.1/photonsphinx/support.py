# flake8: noqa

from pygments.style import Style
from pygments.token import (
    Keyword,
    Name,
    Comment,
    String,
    Error,
    Number,
    Operator,
    Generic,
    Whitespace,
    Punctuation,
    Other,
    Literal,
)


# Originally based on FlaskyStyle which was based on 'tango'.
class photonsphinx(Style):
    background_color = "#000"  # doesn't seem to override CSS 'pre' styling?
    default_style = ""

    styles = {
        # No corresponding class for the following:
        # Text:                     "", # class:  ''
        Whitespace: "underline #f8f8f8",  # class: 'w'
        Error: "#a40000 border:#ef2929",  # class: 'err'
        Other: "#EEE",  # class 'x'
        Comment: "italic #8f5902",  # class: 'c'
        Comment.Preproc: "noitalic",  # class: 'cp'
        Keyword: "bold #004461",  # class: 'k'
        Keyword.Constant: "bold #004461",  # class: 'kc'
        Keyword.Declaration: "bold #004461",  # class: 'kd'
        Keyword.Namespace: "bold #004461",  # class: 'kn'
        Keyword.Pseudo: "bold #004461",  # class: 'kp'
        Keyword.Reserved: "bold #004461",  # class: 'kr'
        Keyword.Type: "bold #004461",  # class: 'kt'
        Operator: "#582800",  # class: 'o'
        Operator.Word: "bold #004461",  # class: 'ow' - like keywords
        Punctuation: "bold #EEE",  # class: 'p'
        # because special names such as Name.Class, Name.Function, etc.
        # are not recognized as such later in the parsing, we choose them
        # to look the same as ordinary variables.
        Name: "#EEE",  # class: 'n'
        Name.Attribute: "#c4a000",  # class: 'na' - to be revised
        Name.Builtin: "#004461",  # class: 'nb'
        Name.Builtin.Pseudo: "#3465a4",  # class: 'bp'
        Name.Class: "#EEE",  # class: 'nc' - to be revised
        Name.Constant: "#EEE",  # class: 'no' - to be revised
        Name.Decorator: "#888",  # class: 'nd' - to be revised
        Name.Entity: "#ce5c00",  # class: 'ni'
        Name.Exception: "bold #cc0000",  # class: 'ne'
        Name.Function: "#EEE",  # class: 'nf'
        Name.Property: "#EEE",  # class: 'py'
        Name.Label: "#f57900",  # class: 'nl'
        Name.Namespace: "#EEE",  # class: 'nn' - to be revised
        Name.Other: "#EEE",  # class: 'nx'
        Name.Tag: "bold #004461",  # class: 'nt' - like a keyword
        Name.Variable: "#EEE",  # class: 'nv' - to be revised
        Name.Variable.Class: "#EEE",  # class: 'vc' - to be revised
        Name.Variable.Global: "#EEE",  # class: 'vg' - to be revised
        Name.Variable.Instance: "#EEE",  # class: 'vi' - to be revised
        Number: "#990000",  # class: 'm'
        Literal: "#EEE",  # class: 'l'
        Literal.Date: "#EEE",  # class: 'ld'
        String: "#4e9a06",  # class: 's'
        String.Backtick: "#4e9a06",  # class: 'sb'
        String.Char: "#4e9a06",  # class: 'sc'
        String.Doc: "italic #8f5902",  # class: 'sd' - like a comment
        String.Double: "#4e9a06",  # class: 's2'
        String.Escape: "#4e9a06",  # class: 'se'
        String.Heredoc: "#4e9a06",  # class: 'sh'
        String.Interpol: "#4e9a06",  # class: 'si'
        String.Other: "#4e9a06",  # class: 'sx'
        String.Regex: "#4e9a06",  # class: 'sr'
        String.Single: "#4e9a06",  # class: 's1'
        String.Symbol: "#4e9a06",  # class: 'ss'
        Generic: "#EEE",  # class: 'g'
        Generic.Deleted: "#a40000",  # class: 'gd'
        Generic.Emph: "italic #EEE",  # class: 'ge'
        Generic.Error: "#ef2929",  # class: 'gr'
        Generic.Heading: "bold #000080",  # class: 'gh'
        Generic.Inserted: "#00A000",  # class: 'gi'
        Generic.Output: "#888",  # class: 'go'
        Generic.Prompt: "#745334",  # class: 'gp'
        Generic.Strong: "bold #EEE",  # class: 'gs'
        Generic.Subheading: "bold #800080",  # class: 'gu'
        Generic.Traceback: "bold #a40000",  # class: 'gt'
    }
