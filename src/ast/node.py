from dataclasses import dataclass
from typing import List, Union, Optional


@dataclass
class ASTNode: ...


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class VarDecl(ASTNode):
    name: str
    value: Optional[int] = None


@dataclass
class Load(ASTNode):
    dest: str  # register
    src: Union[str, int]  # register, identifier, or immediate


@dataclass
class Set(ASTNode):
    dest: str  # identifier
    src: Union[str, int]  # register or immediate


@dataclass
class Move(ASTNode):
    dest: str  # register
    src: str  # register


@dataclass
class BinaryOp(ASTNode):
    op: str  # ADD, SUB, MUL, DIV, AND, OR, XOR
    dest: str  # register
    left: str  # register
    right: Union[str, int]  # register or immediate


@dataclass
class UnaryOp(ASTNode):
    op: str  # INC, DEC, NOT
    operand: str  # register or identifier


@dataclass
class ShiftOp(ASTNode):
    op: str  # SHL, SHR
    dest: str  # register
    src: str  # register
    count: int  # immediate


@dataclass
class Label(ASTNode):
    name: str


@dataclass
class Function(ASTNode):
    name: str
    body: List[ASTNode]


@dataclass
class Call(ASTNode):
    name: str


@dataclass
class Return(ASTNode):
    value: Optional[str] = None  # register or None


@dataclass
class Loop(ASTNode):
    var: str  # identifier
    limit: int
    body: List[ASTNode]


@dataclass
class While(ASTNode):
    condition: "Condition"
    body: List[ASTNode]


@dataclass
class For(ASTNode):
    var: str
    start: int
    end: int
    step: int
    body: List[ASTNode]


@dataclass
class Repeat(ASTNode):
    body: List[ASTNode]
    condition: "Condition"


@dataclass
class If(ASTNode):
    condition: "Condition"
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None


@dataclass
class Condition:
    left: Union[str, int]  # register, identifier, or immediate
    op: str  # ==, !=, >, <, >=, <=
    right: Union[str, int]  # register, identifier, or immediate


@dataclass
class Push(ASTNode):
    register: str


@dataclass
class Pop(ASTNode):
    register: str


@dataclass
class Print(ASTNode):
    value: Union[str, int]  # register, identifier, or immediate


@dataclass
class Input(ASTNode):
    dest: str  # register or identifier

@dataclass
class Halt(ASTNode):
    pass

@dataclass
class Nop(ASTNode):
    pass