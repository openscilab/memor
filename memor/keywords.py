# -*- coding: utf-8 -*-
"""Tokens estimator keywords."""

COMMON_PREFIXES = {"un", "re", "in", "dis", "pre", "mis", "non", "over", "under", "sub", "trans"}

COMMON_SUFFIXES = {"ing", "ed", "ly", "es", "s", "ment", "able", "ness", "tion", "ive", "ous"}

PYTHON_KEYWORDS = {"if", "else", "elif", "while", "for", "def", "return", "import", "from", "class",
                   "try", "except", "finally", "with", "as", "break", "continue", "pass", "lambda",
                   "True", "False", "None", "and", "or", "not", "in", "is", "global", "nonlocal"}

JAVASCRIPT_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "do", "break",
                       "continue", "function", "return", "var", "let", "const", "class", "extends",
                       "super", "import", "export", "try", "catch", "finally", "throw", "new",
                       "delete", "typeof", "instanceof", "in", "void", "yield", "this", "async",
                       "await", "static", "get", "set", "true", "false", "null", "undefined"}

JAVA_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "do", "break",
                 "continue", "return", "void", "int", "float", "double", "char", "long", "short",
                 "boolean", "byte", "class", "interface", "extends", "implements", "new", "import",
                 "package", "public", "private", "protected", "static", "final", "abstract",
                 "try", "catch", "finally", "throw", "throws", "synchronized", "volatile", "transient",
                 "native", "strictfp", "assert", "instanceof", "super", "this", "true", "false", "null"}


C_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "do", "break", "continue",
              "return", "void", "char", "int", "float", "double", "short", "long", "signed",
              "unsigned", "struct", "union", "typedef", "enum", "const", "volatile", "extern",
              "register", "static", "auto", "sizeof", "goto"}


CPP_KEYWORDS = C_KEYWORDS | {"new", "delete", "class",
                             "public", "private", "protected", "namespace", "using", "template", "friend",
                             "virtual", "inline", "operator", "explicit", "this", "true", "false", "nullptr"}


CSHARP_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "do", "break",
                   "continue", "return", "void", "int", "float", "double", "char", "long", "short",
                   "bool", "byte", "class", "interface", "struct", "new", "namespace", "using",
                   "public", "private", "protected", "static", "readonly", "const", "try", "catch",
                   "finally", "throw", "async", "await", "true", "false", "null"}


GO_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "break", "continue", "return",
               "func", "var", "const", "type", "struct", "interface", "map", "chan", "package",
               "import", "defer", "go", "select", "range", "fallthrough", "goto"}


RUST_KEYWORDS = {"if", "else", "match", "loop", "for", "while", "break", "continue", "return",
                 "fn", "let", "const", "static", "struct", "enum", "trait", "impl", "mod",
                 "use", "crate", "super", "self", "as", "type", "where", "pub", "unsafe",
                 "dyn", "move", "async", "await", "true", "false"}


SWIFT_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "repeat", "break",
                  "continue", "return", "func", "var", "let", "class", "struct", "enum", "protocol",
                  "import", "defer", "as", "is", "try", "catch", "throw", "throws", "inout",
                  "guard", "self", "super", "true", "false", "nil"}


KOTLIN_KEYWORDS = {"if", "else", "when", "for", "while", "do", "break", "continue", "return",
                   "fun", "val", "var", "class", "object", "interface", "enum", "sealed",
                   "import", "package", "as", "is", "in", "try", "catch", "finally", "throw",
                   "super", "this", "by", "constructor", "init", "companion", "override",
                   "abstract", "final", "open", "private", "protected", "public", "internal",
                   "inline", "suspend", "operator", "true", "false", "null"}

TYPESCRIPT_KEYWORDS = JAVASCRIPT_KEYWORDS | {"interface", "type", "namespace", "declare"}


PHP_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "do", "break",
                "continue", "return", "function", "class", "public", "private", "protected",
                "extends", "implements", "namespace", "use", "new", "static", "global",
                "const", "var", "echo", "print", "try", "catch", "finally", "throw", "true", "false", "null"}

RUBY_KEYWORDS = {"if", "else", "elsif", "unless", "case", "when", "for", "while", "do", "break",
                 "continue", "return", "def", "class", "module", "end", "begin", "rescue", "ensure",
                 "yield", "super", "self", "alias", "true", "false", "nil"}

SQL_KEYWORDS = {"SELECT", "INSERT", "UPDATE", "DELETE", "FROM", "WHERE", "JOIN", "INNER", "LEFT",
                "RIGHT", "FULL", "ON", "GROUP BY", "HAVING", "ORDER BY", "LIMIT", "OFFSET", "AS",
                "AND", "OR", "NOT", "NULL", "TRUE", "FALSE"}

BASH_KEYWORDS = {"if", "else", "fi", "then", "elif", "case", "esac", "for", "while", "do", "done",
                 "break", "continue", "return", "function", "export", "readonly", "local", "declare",
                 "eval", "trap", "exec", "true", "false"}

MATLAB_KEYWORDS = {"if", "else", "elseif", "end", "for", "while", "break", "continue", "return",
                   "function", "global", "persistent", "switch", "case", "otherwise", "try", "catch",
                   "true", "false"}

R_KEYWORDS = {"if", "else", "repeat", "while", "for", "break", "next", "return", "function",
              "TRUE", "FALSE", "NULL", "Inf", "NaN", "NA"}


PERL_KEYWORDS = {"if", "else", "elsif", "unless", "while", "for", "foreach", "do", "last", "next",
                 "redo", "goto", "return", "sub", "package", "use", "require", "my", "local", "our",
                 "state", "BEGIN", "END", "true", "false"}

LUA_KEYWORDS = {"if", "else", "elseif", "then", "for", "while", "repeat", "until", "break", "return",
                "function", "end", "local", "do", "true", "false", "nil"}

SCALA_KEYWORDS = {"if", "else", "match", "case", "for", "while", "do", "yield", "return",
                  "def", "val", "var", "lazy", "class", "object", "trait", "extends",
                  "with", "import", "package", "new", "this", "super", "implicit",
                  "override", "abstract", "final", "sealed", "private", "protected",
                  "public", "try", "catch", "finally", "throw", "true", "false", "null"}

DART_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "do", "break",
                 "continue", "return", "var", "final", "const", "dynamic", "void",
                 "int", "double", "bool", "String", "class", "interface", "extends",
                 "implements", "mixin", "import", "library", "part", "typedef",
                 "this", "super", "as", "is", "new", "try", "catch", "finally", "throw",
                 "async", "await", "true", "false", "null"}

JULIA_KEYWORDS = {"if", "else", "elseif", "for", "while", "break", "continue", "return",
                  "function", "macro", "module", "import", "using", "export", "struct",
                  "mutable", "const", "begin", "end", "do", "try", "catch", "finally",
                  "true", "false", "nothing"}

HASKELL_KEYWORDS = {"if", "then", "else", "case", "of", "let", "in", "where", "do", "module",
                    "import", "class", "instance", "data", "type", "newtype", "deriving",
                    "default", "foreign", "safe", "unsafe", "qualified", "true", "false"}

COBOL_KEYWORDS = {"ACCEPT", "ADD", "CALL", "CANCEL", "CLOSE", "COMPUTE", "CONTINUE", "DELETE",
                  "DISPLAY", "DIVIDE", "EVALUATE", "EXIT", "GOBACK", "GO", "IF", "INITIALIZE",
                  "INSPECT", "MERGE", "MOVE", "MULTIPLY", "OPEN", "PERFORM", "READ", "RETURN",
                  "REWRITE", "SEARCH", "SET", "SORT", "START", "STOP", "STRING", "SUBTRACT",
                  "UNSTRING", "WRITE", "END-IF", "END-PERFORM"}

OBJECTIVEC_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "do", "break",
                       "continue", "return", "void", "int", "float", "double", "char", "long", "short",
                       "signed", "unsigned", "class", "interface", "protocol", "implementation",
                       "try", "catch", "finally", "throw", "import", "self", "super", "atomic",
                       "nonatomic", "strong", "weak", "retain", "copy", "assign", "true", "false", "nil"}

FSHARP_KEYWORDS = {"if", "then", "else", "match", "with", "for", "while", "do", "done", "let",
                   "rec", "in", "try", "finally", "raise", "exception", "function", "return",
                   "type", "mutable", "namespace", "module", "open", "abstract", "override",
                   "inherit", "base", "new", "true", "false", "null"}

LISP_KEYWORDS = {"defun", "setq", "let", "lambda", "if", "cond", "loop", "dolist", "dotimes",
                 "progn", "return", "function", "defmacro", "quote", "eval", "apply", "car",
                 "cdr", "cons", "list", "mapcar", "format", "read", "print", "load", "t", "nil"}

PROLOG_KEYWORDS = {"if", "else", "end", "fail", "true", "false", "not", "repeat", "is",
                   "assert", "retract", "call", "findall", "bagof", "setof", "atom",
                   "integer", "float", "char_code", "compound", "number", "var"}

ADA_KEYWORDS = {"if", "then", "else", "elsif", "case", "when", "for", "while", "loop", "exit",
                "return", "procedure", "function", "package", "use", "is", "begin", "end",
                "record", "type", "constant", "exception", "raise", "declare", "private",
                "null", "true", "false"}

DELPHI_KEYWORDS = {"if", "then", "else", "case", "of", "for", "while", "repeat", "until", "break",
                   "continue", "begin", "end", "procedure", "function", "var", "const", "type",
                   "class", "record", "interface", "implementation", "unit", "uses", "inherited",
                   "try", "except", "finally", "raise", "private", "public", "protected", "published",
                   "true", "false", "nil"}

VB_KEYWORDS = {"If", "Then", "Else", "ElseIf", "End", "For", "Each", "While", "Do", "Loop",
               "Select", "Case", "Try", "Catch", "Finally", "Throw", "Return", "Function",
               "Sub", "Class", "Module", "Namespace", "Imports", "Inherits", "Implements",
               "Public", "Private", "Protected", "Friend", "Shared", "Static", "Dim", "Const",
               "New", "Me", "MyBase", "MyClass", "Not", "And", "Or", "True", "False", "Nothing"}

HTML_KEYWORDS = {"html", "head", "title", "meta", "link", "style", "script", "body", "div", "span",
                 "h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "img", "ul", "ol", "li", "table",
                 "tr", "td", "th", "thead", "tbody", "tfoot", "form", "input", "button", "label",
                 "select", "option", "textarea", "fieldset", "legend", "iframe", "nav", "section",
                 "article", "aside", "header", "footer", "main", "blockquote", "cite", "code",
                 "pre", "em", "strong", "b", "i", "u", "small", "br", "hr"}

CSS_KEYWORDS = {"color", "background", "border", "margin", "padding", "width", "height", "font-size",
                "font-family", "text-align", "display", "position", "top", "bottom", "left", "right",
                "z-index", "visibility", "opacity", "overflow", "cursor", "flex", "grid", "align-items",
                "justify-content", "box-shadow", "text-shadow", "animation", "transition", "transform",
                "clip-path", "content", "filter", "outline", "max-width", "min-width", "max-height",
                "min-height", "letter-spacing", "line-height", "white-space", "word-break"}


PROGRAMMING_LANGUAGES = {
    "Python": PYTHON_KEYWORDS,
    "JavaScript": JAVASCRIPT_KEYWORDS,
    "Java": JAVA_KEYWORDS,
    "C": C_KEYWORDS,
    "C++": CPP_KEYWORDS,
    "C#": CSHARP_KEYWORDS,
    "Go": GO_KEYWORDS,
    "Rust": RUST_KEYWORDS,
    "Swift": SWIFT_KEYWORDS,
    "Kotlin": KOTLIN_KEYWORDS,
    "TypeScript": TYPESCRIPT_KEYWORDS,
    "PHP": PHP_KEYWORDS,
    "Ruby": RUBY_KEYWORDS,
    "SQL": SQL_KEYWORDS,
    "Bash": BASH_KEYWORDS,
    "MATLAB": MATLAB_KEYWORDS,
    "R": R_KEYWORDS,
    "Perl": PERL_KEYWORDS,
    "Lua": LUA_KEYWORDS,
    "Scala": SCALA_KEYWORDS,
    "Dart": DART_KEYWORDS,
    "Julia": JULIA_KEYWORDS,
    "Haskell": HASKELL_KEYWORDS,
    "COBOL": COBOL_KEYWORDS,
    "Objective-C": OBJECTIVEC_KEYWORDS,
    "F#": FSHARP_KEYWORDS,
    "Lisp": LISP_KEYWORDS,
    "Prolog": PROLOG_KEYWORDS,
    "Ada": ADA_KEYWORDS,
    "Delphi": DELPHI_KEYWORDS,
    "Visual Basic": VB_KEYWORDS,
    "HTML": HTML_KEYWORDS,
    "CSS": CSS_KEYWORDS}

PROGRAMMING_LANGUAGES_KEYWORDS = set()
for language in PROGRAMMING_LANGUAGES:
    PROGRAMMING_LANGUAGES_KEYWORDS = PROGRAMMING_LANGUAGES_KEYWORDS | PROGRAMMING_LANGUAGES[language]
