from dataclasses import dataclass, field
from typing import Any


@dataclass
class ASTNode:
    pass


@dataclass
class Literal(ASTNode):
    value: Any


@dataclass
class VariableReference(ASTNode):
    name: str


@dataclass
class VariableDeclaration(ASTNode):
    var_type: str
    name: str
    value: ASTNode


@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class PrintStatement(ASTNode):
    values: list


@dataclass
class InputStatement(ASTNode):
    prompt: ASTNode
    variable: str


@dataclass
class BinaryOperation(ASTNode):
    operator: str
    left: ASTNode
    right: ASTNode


@dataclass
class UnaryOperation(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    if_body: list
    else_body: list = field(default_factory=list)


@dataclass
class RepeatCountStatement(ASTNode):
    count: ASTNode
    body: list


@dataclass
class RepeatRangeStatement(ASTNode):
    start: ASTNode
    end: ASTNode
    body: list
    var_name: str = "number"


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: list


@dataclass
class ForEachStatement(ASTNode):
    var_name: str
    list_name: str
    body: list


@dataclass
class FunctionDefinition(ASTNode):
    name: str
    params: list
    body: list


@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: list = field(default_factory=list)


@dataclass
class ReturnStatement(ASTNode):
    value: ASTNode


@dataclass
class ListDeclaration(ASTNode):
    name: str
    elements: list


@dataclass
class ListAppend(ASTNode):
    list_name: str
    element: ASTNode


@dataclass
class ListRemove(ASTNode):
    list_name: str
    element: ASTNode


@dataclass
class ListAccess(ASTNode):
    list_name: str
    index: ASTNode


@dataclass
class NoteStatement(ASTNode):
    text: str


@dataclass
class Program(ASTNode):
    statements: list
