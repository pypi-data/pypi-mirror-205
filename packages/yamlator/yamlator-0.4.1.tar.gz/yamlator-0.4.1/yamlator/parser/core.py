"""Maintains the parser transformers"""

import re
import os
import enum

from pathlib import Path
from typing import Iterator
from typing import Any

from lark import Lark
from lark import v_args
from lark import Transformer
from lark import Token
from lark import UnexpectedInput
from lark.exceptions import VisitError

from yamlator.types import Rule
from yamlator.types import ContainerTypes
from yamlator.types import YamlatorRuleset
from yamlator.types import YamlatorEnum
from yamlator.types import YamlatorType
from yamlator.types import PartiallyLoadedYamlatorSchema
from yamlator.types import RuleType
from yamlator.types import UnionRuleType
from yamlator.types import EnumItem
from yamlator.types import SchemaTypes
from yamlator.types import ImportedType
from yamlator.types import ImportStatement
from yamlator.exceptions import NestedUnionError
from yamlator.exceptions import SchemaParseError


_package_dir = Path(__file__).parent.parent.absolute()
_GRAMMAR_FILE = os.path.join(_package_dir, 'grammar/grammar.lark')

_QUOTES_REGEX = re.compile(r'\"|\'')


def parse_schema(schema_content: str) -> PartiallyLoadedYamlatorSchema:
    """Parses a schema into a set of instructions that can be
    used to validate a YAML file.

    Args:
        schema_content (str): The content of a schema

    Returns:
        A `dict` that contains the instructions to validate the YAML file

    Raises:
        ValueError: Raised when `schema_content` is `None`

        yamlator.exceptions.SchemaParseError: Raised when the parsing
            process is interrupted

        yamlator.parser.SchemaSyntaxError: Raised when a syntax error
            is detected in the schema
    """
    if schema_content is None:
        raise ValueError('schema_content should not be None')

    lark_parser = Lark.open(_GRAMMAR_FILE)
    transformer = SchemaTransformer()

    try:
        tokens = lark_parser.parse(schema_content)
        return transformer.transform(tokens)
    except VisitError as ve:
        raise SchemaParseError(ve.orig_exc) from ve
    except UnexpectedInput as u:
        _handle_syntax_errors(u, lark_parser, schema_content)


class SchemaTransformer(Transformer):
    """Transforms the schema contents into a set of objects that
    can be used to validate a YAML file. This class will be used by Lark
    during the parsing process.

    Each method matches to a terminal or rule in the grammar (.lark) file.
    E.g the method `required_rule` corresponds to the following rule
    in the grammar:

    required_rule: rule_name type "required" NEW_LINES
                 | rule_name type NEW_LINES
    """

    def __init__(self, visit_tokens: bool = True) -> None:
        super().__init__(visit_tokens)

        # Used to track previously seen enums or rulesets to dynamically
        # determine the type of the rule is a enum or ruleset
        self.seen_constructs = {}
        self.unknown_types = []

    def rule_name(self, tokens: Iterator[Token]) -> Token:
        """Processes the rule name by removing any quotes"""
        token = tokens[0]
        name = token.value.strip()
        name = _QUOTES_REGEX.sub('', name)
        return Token(value=name, type_=token.type)

    def required_rule(self, tokens: Iterator[Token]) -> Rule:
        """Transforms the required rule tokens in a Rule object"""
        (name, rtype) = tokens[0:2]
        return Rule(name.value, rtype, True)

    def optional_rule(self, tokens: Iterator[Token]) -> Rule:
        """Transforms the optional rule tokens in a Rule object"""
        (name, rtype) = tokens[0:2]
        return Rule(name.value, rtype, False)

    def ruleset(self, tokens: Iterator[Token]) -> YamlatorRuleset:
        """Transforms the ruleset tokens into a YamlatorRuleset object"""
        is_strict = False
        if tokens[0].type == GrammarKeywords.STRICT:
            tokens = tokens[1:]
            is_strict = True

        name = tokens[0].value
        rules = tokens[1:]

        self.seen_constructs[name] = SchemaTypes.RULESET
        parent_token = tokens[1]
        if isinstance(parent_token, RuleType):
            return YamlatorRuleset(name, tokens[2:], is_strict, parent_token)
        return YamlatorRuleset(name, rules, is_strict)

    def ruleset_parent(self, tokens: Iterator[RuleType]) -> RuleType:
        """Extracts the ruleset parent from the token list"""
        # This method is needed to prevent Lark from wrapping the tokens
        # a tree object
        return tokens[0]

    def start(self, instructions: Iterator[YamlatorType]) \
            -> PartiallyLoadedYamlatorSchema:
        """Transforms the instructions into a dict that sorts the rulesets,
        enums and entry point to validate the YAML data"""
        root = None
        rules = {}
        enums = {}
        imports = []

        enum_handler = _EnumInstructionHandler(enums)
        handler_chain = _RulesetInstructionHandler(rules)
        handler_chain.set_next_handler(enum_handler)
        enum_handler.set_next_handler(_ImportInstructionHandler(imports))

        for instruction in instructions:
            handler_chain.handle(instruction)

        root = rules.get('main')
        if root is not None:
            del rules['main']

        return PartiallyLoadedYamlatorSchema(root, rules, enums,
                                             imports, self.unknown_types)

    def str_type(self, _: Iterator[Token]) -> RuleType:
        """Transforms a string type token into a RuleType object"""
        return RuleType(schema_type=SchemaTypes.STR)

    def int_type(self, _: Iterator[Token]) -> RuleType:
        """Transforms a int type token into a RuleType object"""
        return RuleType(schema_type=SchemaTypes.INT)

    def float_type(self, _: Iterator[Token]) -> RuleType:
        """Transforms a float type token into a RuleType object"""
        return RuleType(schema_type=SchemaTypes.FLOAT)

    def list_type(self, tokens: Iterator[Token]) -> RuleType:
        """Transforms a list type token into a RuleType object"""
        return RuleType(schema_type=SchemaTypes.LIST, sub_type=tokens[0])

    def map_type(self, tokens: Iterator[Token]) -> RuleType:
        """Transforms a map type token into a RuleType object"""
        return RuleType(schema_type=SchemaTypes.MAP, sub_type=tokens[0])

    def any_type(self, _: Iterator[Token]) -> RuleType:
        """Transforms the any type token into a RuleType object"""
        return RuleType(schema_type=SchemaTypes.ANY)

    def bool_type(self, _: Iterator[Token]) -> RuleType:
        """Transforms a bool type token into a RuleType object"""
        return RuleType(schema_type=SchemaTypes.BOOL)

    def enum_item(self, tokens: Iterator[Token]) -> EnumItem:
        """Transforms a enum item token into a EnumItem object"""
        name, value = tokens
        return EnumItem(name=name, value=value)

    def enum(self, tokens: Iterator[Token]) -> YamlatorEnum:
        """Transforms a enum token into a YamlatorEnum object"""
        enums = {}

        name = tokens[0]
        items = tokens[1:]

        for item in items:
            enums[item.value] = item
        self.seen_constructs[name] = SchemaTypes.ENUM
        return YamlatorEnum(name.value, enums)

    def container_type(self, tokens: Iterator[Token]) -> RuleType:
        """Transforms a container type token into a RuleType object

        Raises:
            yamlator.exceptions.ConstructNotFoundError: Raised if the
                enum or ruleset cannot be found
        """
        name = tokens[0]
        if len(tokens) > 1:
            name = f'{tokens[0]}.{tokens[1]}'
        else:
            name = name.value

        schema_type = self.seen_constructs.get(name, SchemaTypes.UNKNOWN)
        rule_type = RuleType(schema_type=schema_type, lookup=name)
        if schema_type == SchemaTypes.UNKNOWN:
            self.unknown_types.append(rule_type)
        return rule_type

    def regex_type(self, tokens: Iterator[Token]) -> RuleType:
        """Transforms a regex type token into a RuleType object"""
        (regex, ) = tokens
        return RuleType(schema_type=SchemaTypes.REGEX, regex=regex)

    def union_type(self, tokens: 'list[RuleType]'):
        """Transforms a union token into a Union RuleType

        Raises:
            yamlator.exceptions.NestedUnionError: Raised if the tokens
                contains a union RuleType which indicates a nested
                union within the union
        """
        for token in tokens:
            if token.schema_type == SchemaTypes.UNION:
                raise NestedUnionError()
        return UnionRuleType(sub_types=tokens)

    def type(self, tokens: Iterator[Token]) -> Any:
        """Extracts the type tokens and passes them onto
        the next stage in the transformer
        """
        (t, ) = tokens
        return t

    def schema_entry(self, tokens: list) -> YamlatorRuleset:
        """Transforms the schema entry point token into a YamlatorRuleset called
        main that will act as the entry point for validating the YAML data
        """
        first_token = tokens[0]

        # If the first item is not a `lark.Token`
        # then the tokens in the list are all rules
        if not isinstance(first_token, Token):
            return YamlatorRuleset('main', tokens)

        # If the first type is `lark.Token` then the
        # first token is an indicator it is in strict mode
        return YamlatorRuleset('main', tokens[1:], True)

    @v_args(inline=True)
    def integer(self, token: str) -> int:
        """Converts a integer string into a int type"""
        return int(token)

    @v_args(inline=True)
    def float(self, token: str) -> float:
        """Converts a float string into a int type"""
        return float(token)

    @v_args(inline=True)
    def string(self, token: str) -> str:
        """Transforms the escaped string by removing quotes
        from the value
        """
        return _QUOTES_REGEX.sub('', token)

    def import_statement(self, tokens: Iterator[Token]) -> ImportStatement:
        """Transforms an import statement into a
        `yamlator.types.ImportStatement` object
        """
        items: Iterator[Token] = tokens[0]

        path = tokens[1]
        path = _QUOTES_REGEX.sub('', path.value)

        namespace = None
        try:
            namespace = tokens[2].value
        except IndexError:
            pass

        statements = []
        for item in items:
            statements.append(ImportedType(item.value, path, namespace))
        return ImportStatement(statements)

    def imported_types(self, tokens: Iterator[Token]) -> Iterator[Token]:
        # This method is needed to prevent Lark from wrapping the tokens
        # a tree object
        return tokens


class GrammarKeywords(str, enum.Enum):
    STRICT = 'STRICT_KEYWORD'


class _InstructionHandler:
    """Base handle for dealing with Yamlator types"""

    _next_handler = None

    def set_next_handler(self,
                         handler: '_InstructionHandler'
                         ) -> '_InstructionHandler':
        """Set the next handler in the chain

        Args:
            handler (yamlator.parser._InstructionHandler): The next
                instruction handler

        Returns:
            The instance of the instruction handler that was
            passed as an argument
        """
        self._next_handler = handler
        return handler

    def handle(self, instruction: YamlatorType) -> None:
        if self._next_handler is not None:
            self._next_handler.handle(instruction)


class _EnumInstructionHandler(_InstructionHandler):
    """Enum type instruction handler"""

    def __init__(self, enums: dict):
        super().__init__()
        self._enums = enums

    def handle(self, instruction: YamlatorType) -> None:
        if instruction.container_type != ContainerTypes.ENUM:
            super().handle(instruction)
            return

        self._enums[instruction.name] = instruction


class _RulesetInstructionHandler(_InstructionHandler):
    """Ruleset type instruction handler"""

    def __init__(self, rulesets: dict):
        super().__init__()
        self._rulesets = rulesets

    def handle(self, instruction: YamlatorType) -> None:
        if instruction.container_type != ContainerTypes.RULESET:
            super().handle(instruction)
            return

        self._rulesets[instruction.name] = instruction


class _ImportInstructionHandler(_InstructionHandler):
    """Import statement handler for putting all the
    import statements into a single data structure
    """

    def __init__(self, imports: list):
        """_ImportInstructionHandler init

        imports (list): Reference to a list that will store all the
            import statements that were referenced in the Yamlator schema
        """
        super().__init__()
        self.imports = imports

    def handle(self, instruction: YamlatorType) -> None:
        if instruction.container_type != ContainerTypes.IMPORT:
            super().handle(instruction)
            return

        instruction: ImportStatement = instruction
        self.imports.extend(instruction.imports)


class SchemaSyntaxError(SyntaxError):
    """A generic syntax error in the schema content"""

    label = None

    def __str__(self) -> str:
        context, line, column, *_ = self.args
        if self.label is None:
            return f'Error on line {line}, column {column}.\n\n{context}'
        return f'{self.label} at line {line}, column {column}.\n\n{context}'


class MalformedRulesetNameError(SchemaSyntaxError):
    """Indicates an error in the ruleset name"""
    label = 'Invalid ruleset name'


class MalformedEnumNameError(SchemaSyntaxError):
    """Indicates an error in the enum name"""
    label = 'Invalid enum name'


class MissingRulesError(SchemaSyntaxError):
    """Indicates that a ruleset or schema block is missing rules"""
    label = 'Missing rules'


def _handle_syntax_errors(u: UnexpectedInput, parser: Lark,
                          content: str) -> None:
    exc_class = u.match_examples(parser.parse, {
        MalformedRulesetNameError: [
            'ruleset foo',
            'ruleset 1234Foo',
            'ruleset FOO',
        ],
        MalformedEnumNameError: [
            'enum foo',
            'enum 1234Foo',
            'enum FOO',
        ],
        MissingRulesError: [
            'ruleset Foo {}',
            'schema {}'
        ]
    }, use_accepts=True)
    if not exc_class:
        raise SchemaSyntaxError(u.get_context(content), u.line, u.column)
    raise exc_class(u.get_context(content), u.line, u.column)
