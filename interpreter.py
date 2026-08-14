from dataclasses import dataclass, field
import os
import sys
from datetime import datetime
from ast_nodes import (
    Program, Literal, VariableReference, VariableDeclaration, Assignment,
    PrintStatement, InputStatement, BinaryOperation, UnaryOperation,
    IfStatement, RepeatCountStatement, RepeatRangeStatement, WhileStatement,
    ForEachStatement, FunctionDefinition, FunctionCall, ReturnStatement,
    ListDeclaration, ListAppend, ListRemove, NoteStatement,
    DictLiteral, MemberAccess, MethodCall, ImportStatement,
)


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class RuntimeError(Exception):
    def __init__(self, message):
        super().__init__(f"Runtime error: {message}")


class BuiltinFunction:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.params = []

    def __call__(self, *args):
        return self.func(args)


@dataclass
class Scope:
    variables: dict = field(default_factory=dict)
    parent: "Scope" = None

    def get(self, name: str):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Variable '{name}' is not defined")

    def set(self, name: str, value):
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent:
            try:
                self.parent.set(name, value)
                return
            except RuntimeError:
                pass
        self.variables[name] = value

    def create(self, name: str, value):
        self.variables[name] = value


class Interpreter:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.functions = {}
        self._register_builtins()

    def _register_builtins(self):
        self.functions["database"] = BuiltinFunction("database", self._builtin_database)
        self.functions["now"] = BuiltinFunction("now", self._builtin_now)
        self.functions["len"] = BuiltinFunction("len", self._builtin_len)
        self.functions["str"] = BuiltinFunction("str", self._builtin_str)
        self.functions["num"] = BuiltinFunction("num", self._builtin_num)
        self.functions["input"] = BuiltinFunction("input", self._builtin_input)

    def _builtin_database(self, args):
        if len(args) != 1:
            raise RuntimeError("database() expects exactly 1 argument")
        from database import DatabaseCollection
        return DatabaseCollection(args[0])

    def _builtin_now(self, args):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _builtin_len(self, args):
        if len(args) != 1:
            raise RuntimeError("len() expects exactly 1 argument")
        return len(args[0])

    def _builtin_str(self, args):
        if len(args) != 1:
            raise RuntimeError("str() expects exactly 1 argument")
        return str(args[0])

    def _builtin_num(self, args):
        if len(args) != 1:
            raise RuntimeError("num() expects exactly 1 argument")
        val = args[0]
        if isinstance(val, str):
            if "." in val:
                return float(val)
            return int(val)
        return val

    def _builtin_input(self, args):
        if len(args) == 1:
            value = input(f"{args[0]}: ")
        else:
            value = input()
        return value

    def run(self, program: Program):
        for statement in program.statements:
            self.execute(statement)

    def execute(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.execute(stmt)
        elif isinstance(node, VariableDeclaration):
            value = self.evaluate(node.value)
            self.current_scope.create(node.name, value)
        elif isinstance(node, Assignment):
            value = self.evaluate(node.value)
            self.current_scope.set(node.name, value)
        elif isinstance(node, PrintStatement):
            values = []
            for v in node.values:
                val = self.evaluate(v)
                if isinstance(val, bool):
                    values.append("true" if val else "false")
                elif isinstance(val, float) and val == int(val):
                    values.append(str(int(val)))
                elif isinstance(val, dict):
                    parts = []
                    for k, v2 in val.items():
                        parts.append(f"{k}: {v2}")
                    values.append("{" + ", ".join(parts) + "}")
                elif isinstance(val, list):
                    values.append(str(val))
                else:
                    values.append(str(val))
            print(" ".join(values))
        elif isinstance(node, InputStatement):
            prompt = self.evaluate(node.prompt)
            value = input(f"{prompt}: ")
            self.current_scope.set(node.variable, value)
        elif isinstance(node, IfStatement):
            condition = self.evaluate(node.condition)
            if condition:
                for stmt in node.if_body:
                    self.execute(stmt)
            else:
                for stmt in node.else_body:
                    self.execute(stmt)
        elif isinstance(node, RepeatCountStatement):
            count = self.evaluate(node.count)
            for _ in range(int(count)):
                for stmt in node.body:
                    self.execute(stmt)
        elif isinstance(node, RepeatRangeStatement):
            start = int(self.evaluate(node.start))
            end = int(self.evaluate(node.end))
            for i in range(start, end + 1):
                self.current_scope.set(node.var_name, i)
                for stmt in node.body:
                    self.execute(stmt)
        elif isinstance(node, WhileStatement):
            while self.evaluate(node.condition):
                for stmt in node.body:
                    self.execute(stmt)
        elif isinstance(node, ForEachStatement):
            items = self.current_scope.get(node.list_name)
            for item in items:
                self.current_scope.set(node.var_name, item)
                for stmt in node.body:
                    self.execute(stmt)
        elif isinstance(node, FunctionDefinition):
            self.functions[node.name] = node
        elif isinstance(node, FunctionCall):
            self.call_function(node.name, node.arguments)
        elif isinstance(node, MethodCall):
            self.evaluate(node)
        elif isinstance(node, ReturnStatement):
            value = self.evaluate(node.value)
            raise ReturnException(value)
        elif isinstance(node, ListDeclaration):
            elements = [self.evaluate(e) for e in node.elements]
            self.current_scope.create(node.name, elements)
        elif isinstance(node, ListAppend):
            lst = self.current_scope.get(node.list_name)
            element = self.evaluate(node.element)
            lst.append(element)
        elif isinstance(node, ListRemove):
            lst = self.current_scope.get(node.list_name)
            element = self.evaluate(node.element)
            if element in lst:
                lst.remove(element)
        elif isinstance(node, NoteStatement):
            pass  # comments are ignored
        elif isinstance(node, ImportStatement):
            self.execute_import(node)

    def evaluate(self, node):
        if isinstance(node, Literal):
            return node.value
        elif isinstance(node, VariableReference):
            if node.name == "input":
                return self.call_function("input", [])
            return self.current_scope.get(node.name)
        elif isinstance(node, BinaryOperation):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return self.apply_binary_op(node.operator, left, right)
        elif isinstance(node, UnaryOperation):
            operand = self.evaluate(node.operand)
            if node.operator == "not":
                return not operand
        elif isinstance(node, FunctionCall):
            return self.call_function(node.name, node.arguments)
        elif isinstance(node, DictLiteral):
            result = {}
            for key, value in zip(node.keys, node.values):
                result[key] = self.evaluate(value)
            return result
        elif isinstance(node, MemberAccess):
            obj = self.evaluate(node.object)
            if isinstance(obj, dict):
                if node.property in obj:
                    return obj[node.property]
                raise RuntimeError(f"Key '{node.property}' not found in dictionary")
            return getattr(obj, node.property)
        elif isinstance(node, MethodCall):
            obj = self.evaluate(node.object)
            args = [self.evaluate(arg) for arg in node.arguments]
            method = getattr(obj, node.method)
            return method(*args)
        raise RuntimeError(f"Cannot evaluate {type(node).__name__}")

    def execute_import(self, node):
        filepath = node.filepath
        if not os.path.isabs(filepath):
            caller_dir = os.environ.get("DIPJO_CWD", os.getcwd())
            filepath = os.path.join(caller_dir, filepath)
        if not os.path.exists(filepath):
            raise RuntimeError(f"Cannot import '{node.filepath}': file not found")
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        from lexer import Lexer
        from parser import Parser
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        self.run(program)

    def apply_binary_op(self, op, left, right):
        if op == "plus":
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif op == "minus":
            return left - right
        elif op == "times":
            return left * right
        elif op == "divided_by":
            if right == 0:
                raise RuntimeError("Division by zero")
            if isinstance(left, float) or isinstance(right, float):
                return left / right
            return left // right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        elif op == "and":
            return left and right
        elif op == "or":
            return left or right
        raise RuntimeError(f"Unknown operator: {op}")

    def call_function(self, name, arguments):
        if name not in self.functions:
            raise RuntimeError(f"Function '{name}' is not defined")

        func = self.functions[name]
        args = [self.evaluate(arg) for arg in arguments]

        if isinstance(func, BuiltinFunction):
            return func(*args)

        func_def = func
        if len(args) != len(func_def.params):
            raise RuntimeError(
                f"Function '{name}' expects {len(func_def.params)} arguments but got {len(args)}"
            )

        func_scope = Scope(parent=self.current_scope)
        for param, arg in zip(func_def.params, args):
            func_scope.create(param, arg)

        old_scope = self.current_scope
        self.current_scope = func_scope

        result = None
        try:
            for stmt in func_def.body:
                self.execute(stmt)
        except ReturnException as e:
            result = e.value
        finally:
            self.current_scope = old_scope

        return result
