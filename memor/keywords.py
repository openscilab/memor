# -*- coding: utf-8 -*-
"""Keywords."""

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


CPP_KEYWORDS = {"if", "else", "switch", "case", "default", "for", "while", "do", "break",
                "continue", "return", "void", "char", "int", "float", "double", "short", "long",
                "signed", "unsigned", "struct", "union", "typedef", "enum", "const", "volatile",
                "extern", "register", "static", "auto", "sizeof", "goto", "new", "delete", "class",
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

PROGRAMMING_LANGUAGES = {"Python": PYTHON_KEYWORDS, "JavaScript": JAVASCRIPT_KEYWORDS, "Java": JAVA_KEYWORDS, "C": C_KEYWORDS, "C++": CPP_KEYWORDS, "C#": CSHARP_KEYWORDS, "Go": GO_KEYWORDS,
                         "Rust": RUST_KEYWORDS, "Swift": SWIFT_KEYWORDS, "Kotlin": KOTLIN_KEYWORDS, "TypeScript": TYPESCRIPT_KEYWORDS, "PHP": PHP_KEYWORDS, "Ruby": RUBY_KEYWORDS, "SQL": SQL_KEYWORDS}

PROGRAMMING_LANGUAGES_KEYWORDS = set()
for language in PROGRAMMING_LANGUAGES:
    PROGRAMMING_LANGUAGES_KEYWORDS = PROGRAMMING_LANGUAGES_KEYWORDS | PROGRAMMING_LANGUAGES[language]