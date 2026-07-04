from lexer import Token, TokenType
from ast_nodes import (
    Program, Literal, VariableReference, VariableDeclaration, Assignment,
    PrintStatement, InputStatement, BinaryOperation, UnaryOperation,
    IfStatement, RepeatCountStatement, RepeatRangeStatement, WhileStatement,
    ForEachStatement, FunctionDefinition, FunctionCall, ReturnStatement,
    ListDeclaration, ListAppend, ListRemove, NoteStatement,
)


class ParseError(Exception):
    def __init__(self, message, token):
        super().__init__(
            f"Parse error at line {token.line}, column {token.column}: {message}"
        )
        self.token = token


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF

    def peek_ahead(self, offset=1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def advance(self) -> Token:
        token = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def expect(self, token_type, value=None) -> Token:
        token = self.peek()
        if token.type != token_type:
            raise ParseError(
                f"Expected {token_type.name} but got {token.type.name} ({token.value!r})",
                token,
            )
        if value is not None and token.value != value:
            raise ParseError(
                f"Expected {value!r} but got {token.value!r}", token
            )
        return self.advance()

    def skip_newlines(self):
        while self.peek().type == TokenType.NEWLINE:
            self.advance()

    def skip_commas_and_newlines(self):
        while self.peek().type in (TokenType.COMMA, TokenType.NEWLINE):
            self.advance()

    def parse(self) -> Program:
        statements = []
        self.skip_newlines()
        while self.peek().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self.skip_newlines()
        return Program(statements)

    def parse_statement(self):
        token = self.peek()
        if token.type != TokenType.WORD:
            self.advance()
            return None

        word = token.value.lower()

        if word == "note":
            return self.parse_note()
        elif word == "create":
            return self.parse_create()
        elif word == "remember":
            return self.parse_remember()
        elif word == "set":
            return self.parse_set()
        elif word == "say":
            return self.parse_say()
        elif word == "ask":
            return self.parse_ask()
        elif word == "if":
            return self.parse_if()
        elif word == "repeat":
            return self.parse_repeat()
        elif word == "while":
            return self.parse_while()
        elif word == "for":
            return self.parse_for_each()
        elif word == "define":
            return self.parse_define()
        elif word == "run":
            return self.parse_run()
        elif word == "give":
            return self.parse_give_back()
        elif word == "add":
            return self.parse_add()
        elif word == "subtract":
            return self.parse_subtract()
        elif word == "multiply":
            return self.parse_multiply()
        elif word == "divide":
            return self.parse_divide()
        elif word == "increase":
            return self.parse_increase()
        elif word == "decrease":
            return self.parse_decrease()
        elif word == "put":
            return self.parse_put()
        elif word == "remove":
            return self.parse_remove()
        else:
            raise ParseError(f"Unknown statement starting with '{token.value}'", token)

    def parse_note(self):
        self.advance()  # consume 'note'
        text_parts = []
        while self.peek().type not in (TokenType.PERIOD, TokenType.EOF, TokenType.NEWLINE):
            text_parts.append(self.advance().value)
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return NoteStatement(" ".join(text_parts))

    def parse_expression(self):
        return self.parse_or_expression()

    def parse_or_expression(self):
        left = self.parse_and_expression()
        while self.peek().type == TokenType.WORD and self.peek().value.lower() == "or":
            self.advance()
            right = self.parse_and_expression()
            left = BinaryOperation("or", left, right)
        return left

    def parse_and_expression(self):
        left = self.parse_not_expression()
        while self.peek().type == TokenType.WORD and self.peek().value.lower() == "and":
            if self._is_statement_keyword_ahead():
                break
            self.advance()
            right = self.parse_not_expression()
            left = BinaryOperation("and", left, right)
        return left

    def _is_statement_keyword_ahead(self):
        if self.peek().type != TokenType.WORD:
            return False
        word = self.peek().value.lower()
        if word == "and":
            next_word = self.peek_ahead(1).value.lower() if self.peek_ahead(1).type == TokenType.WORD else ""
            return next_word in ("save", "into", "from", "times", "by", "to", "finish")
        return word in ("save", "into", "from", "times", "by", "to", "finish")

    def parse_not_expression(self):
        if self.peek().type == TokenType.WORD and self.peek().value.lower() == "not":
            self.advance()
            operand = self.parse_comparison()
            return UnaryOperation("not", operand)
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_additive()
        if self.peek().type == TokenType.WORD:
            word = self.peek().value.lower()
            if word == "is":
                self.advance()
                next_word = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
                if next_word == "not":
                    self.advance()
                    next2 = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
                    if next2 == "equal":
                        self.advance()
                        self.expect_word("to")
                        right = self.parse_additive()
                        return BinaryOperation("!=", left, right)
                    elif next2 == "greater":
                        self.advance()
                        self.expect_word("than")
                        right = self.parse_additive()
                        return BinaryOperation("<=", left, right)
                    elif next2 == "less":
                        self.advance()
                        self.expect_word("than")
                        right = self.parse_additive()
                        return BinaryOperation(">=", left, right)
                elif next_word == "equal":
                    self.advance()
                    self.expect_word("to")
                    right = self.parse_additive()
                    return BinaryOperation("==", left, right)
                elif next_word == "greater":
                    self.advance()
                    self.expect_word("than")
                    next3 = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
                    if next3 == "or":
                        self.advance()
                        self.expect_word("equal")
                        self.expect_word("to")
                        right = self.parse_additive()
                        return BinaryOperation(">=", left, right)
                    right = self.parse_additive()
                    return BinaryOperation(">", left, right)
                elif next_word == "less":
                    self.advance()
                    self.expect_word("than")
                    next3 = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
                    if next3 == "or":
                        self.advance()
                        self.expect_word("equal")
                        self.expect_word("to")
                        right = self.parse_additive()
                        return BinaryOperation("<=", left, right)
                    right = self.parse_additive()
                    return BinaryOperation("<", left, right)
                else:
                    right = self.parse_additive()
                    return BinaryOperation("==", left, right)
        return left

    def expect_word(self, expected):
        token = self.peek()
        if token.type != TokenType.WORD or token.value.lower() != expected:
            raise ParseError(f"Expected '{expected}' but got '{token.value}'", token)
        return self.advance()

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.peek().type == TokenType.WORD and self.peek().value.lower() in ("plus", "minus"):
            op = self.advance().value.lower()
            right = self.parse_multiplicative()
            left = BinaryOperation(op, left, right)
        return left

    def parse_multiplicative(self):
        left = self.parse_primary()
        while self.peek().type == TokenType.WORD and self.peek().value.lower() in ("times", "divided"):
            next_after = self.peek_ahead(1)
            if next_after.type in (TokenType.PERIOD, TokenType.COMMA, TokenType.NEWLINE, TokenType.EOF):
                break
            if self.peek().value.lower() == "times" and next_after.type == TokenType.WORD and next_after.value.lower() in ("times", "finish", "and", "or"):
                break
            op_token = self.advance()
            if op_token.value.lower() == "divided":
                self.expect_word("by")
                op = "divided_by"
            else:
                op = "times"
            right = self.parse_primary()
            left = BinaryOperation(op, left, right)
        return left

    def parse_primary(self):
        token = self.peek()

        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)

        if token.type == TokenType.NUMBER:
            self.advance()
            if "." in token.value:
                return Literal(float(token.value))
            return Literal(int(token.value))

        if token.type == TokenType.WORD:
            word = token.value.lower()
            if word == "true":
                self.advance()
                return Literal(True)
            elif word == "false":
                self.advance()
                return Literal(False)
            elif word == "run":
                return self.parse_run_expression()
            else:
                self.advance()
                return VariableReference(token.value)

        raise ParseError(f"Unexpected token: {token.value!r}", token)

    def parse_create(self):
        self.advance()  # consume 'create'
        next_word = self.peek().value.lower()

        if next_word == "list":
            return self.parse_create_list()

        var_type = next_word
        self.advance()  # consume type
        name_token = self.expect(TokenType.WORD)
        self.expect_word("as")
        value = self.parse_expression()
        return VariableDeclaration(var_type, name_token.value, value)

    def parse_create_list(self):
        self.advance()  # consume 'list'
        name_token = self.expect(TokenType.WORD)
        self.expect_word("as")
        elements = []
        elements.append(self.parse_expression())
        while self.peek().type == TokenType.COMMA:
            self.advance()
            if self.peek().type in (TokenType.PERIOD, TokenType.EOF):
                break
            elements.append(self.parse_expression())
        return ListDeclaration(name_token.value, elements)

    def parse_remember(self):
        self.advance()  # consume 'remember'
        name_token = self.expect(TokenType.WORD)
        self.expect_word("as")
        value = self.parse_expression()
        return VariableDeclaration("number", name_token.value, value)

    def parse_set(self):
        self.advance()  # consume 'set'
        name_token = self.expect(TokenType.WORD)
        self.expect_word("to")
        value = self.parse_expression()
        return Assignment(name_token.value, value)

    def parse_say(self):
        self.advance()  # consume 'say'
        values = []
        values.append(self.parse_expression())
        while self.peek().type == TokenType.COMMA:
            self.advance()
            if self.peek().type in (TokenType.PERIOD, TokenType.EOF):
                break
            values.append(self.parse_expression())
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return PrintStatement(values)

    def parse_ask(self):
        self.advance()  # consume 'ask'
        prompt = self.parse_expression()
        self.expect_word("and")
        self.expect_word("save")
        self.expect_word("in")
        var_name = self.expect(TokenType.WORD)
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return InputStatement(prompt, var_name.value)

    def parse_if(self):
        self.advance()  # consume 'if'
        condition = self.parse_expression()
        self.skip_commas_and_newlines()

        if_body = []
        while self.peek().type != TokenType.EOF:
            word = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
            if word == "otherwise" or word == "finish":
                break
            stmt = self.parse_statement()
            if stmt is not None:
                if_body.append(stmt)

        else_body = []
        if self.peek().type == TokenType.WORD and self.peek().value.lower() == "otherwise":
            self.advance()
            self.skip_commas_and_newlines()
            while self.peek().type != TokenType.EOF:
                word = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
                if word == "finish":
                    break
                stmt = self.parse_statement()
                if stmt is not None:
                    else_body.append(stmt)

        self.expect_word("finish")
        self.expect_word("condition")
        if self.peek().type == TokenType.PERIOD:
            self.advance()

        return IfStatement(condition, if_body, else_body)

    def parse_repeat(self):
        self.advance()  # consume 'repeat'
        next_word = self.peek().value.lower()

        if next_word == "from":
            return self.parse_repeat_range()
        else:
            return self.parse_repeat_count()

    def parse_repeat_count(self):
        count = self.parse_expression()
        self.expect_word("times")
        self.skip_commas_and_newlines()

        body = []
        while self.peek().type != TokenType.EOF:
            word = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
            if word == "finish":
                break
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)

        self.expect_word("finish")
        self.expect_word("repeat")
        if self.peek().type == TokenType.PERIOD:
            self.advance()

        return RepeatCountStatement(count, body)

    def parse_repeat_range(self):
        self.advance()  # consume 'from'
        start = self.parse_expression()
        self.expect_word("to")
        end = self.parse_expression()
        self.skip_commas_and_newlines()

        body = []
        while self.peek().type != TokenType.EOF:
            word = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
            if word == "finish":
                break
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)

        self.expect_word("finish")
        self.expect_word("repeat")
        if self.peek().type == TokenType.PERIOD:
            self.advance()

        return RepeatRangeStatement(start, end, body)

    def parse_while(self):
        self.advance()  # consume 'while'
        condition = self.parse_expression()
        self.skip_commas_and_newlines()

        body = []
        while self.peek().type != TokenType.EOF:
            word = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
            if word == "finish":
                break
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)

        self.expect_word("finish")
        self.expect_word("while")
        if self.peek().type == TokenType.PERIOD:
            self.advance()

        return WhileStatement(condition, body)

    def parse_for_each(self):
        self.advance()  # consume 'for'
        self.expect_word("every")
        var_name = self.expect(TokenType.WORD)
        self.expect_word("in")
        list_name = self.expect(TokenType.WORD)
        self.skip_commas_and_newlines()

        body = []
        while self.peek().type != TokenType.EOF:
            word = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
            if word == "finish":
                break
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)

        self.expect_word("finish")
        self.expect_word("loop")
        if self.peek().type == TokenType.PERIOD:
            self.advance()

        return ForEachStatement(var_name.value, list_name.value, body)

    def parse_define(self):
        self.advance()  # consume 'define'
        self.expect_word("function")
        name_token = self.expect(TokenType.WORD)

        params = []
        if self.peek().type == TokenType.WORD and self.peek().value.lower() == "using":
            self.advance()
            params.append(self.expect(TokenType.WORD).value)
            while self.peek().type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.WORD).value)

        if self.peek().type == TokenType.PERIOD:
            self.advance()

        body = []
        while self.peek().type != TokenType.EOF:
            word = self.peek().value.lower() if self.peek().type == TokenType.WORD else ""
            if word == "finish":
                break
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)

        self.expect_word("finish")
        self.expect_word("function")
        if self.peek().type == TokenType.PERIOD:
            self.advance()

        return FunctionDefinition(name_token.value, params, body)

    def parse_run(self):
        self.advance()  # consume 'run'
        self.expect_word("function")
        name_token = self.expect(TokenType.WORD)

        arguments = []
        if self.peek().type == TokenType.WORD and self.peek().value.lower() == "using":
            self.advance()
            arguments.append(self.parse_expression())
            while self.peek().type == TokenType.COMMA:
                self.advance()
                if self.peek().type in (TokenType.PERIOD, TokenType.EOF):
                    break
                arguments.append(self.parse_expression())

        if self.peek().type == TokenType.PERIOD:
            self.advance()

        return FunctionCall(name_token.value, arguments)

    def parse_run_expression(self):
        self.advance()  # consume 'run'
        self.expect_word("function")
        name_token = self.expect(TokenType.WORD)

        arguments = []
        if self.peek().type == TokenType.WORD and self.peek().value.lower() == "using":
            self.advance()
            arguments.append(self.parse_expression())
            while self.peek().type == TokenType.COMMA:
                self.advance()
                arguments.append(self.parse_expression())

        return FunctionCall(name_token.value, arguments)

    def parse_give_back(self):
        self.advance()  # consume 'give'
        self.expect_word("back")
        value = self.parse_expression()
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return ReturnStatement(value)

    def parse_add(self):
        self.advance()  # consume 'add'
        value = self.parse_expression()
        self.expect_word("to")
        name_token = self.expect(TokenType.WORD)
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return Assignment(
            name_token.value,
            BinaryOperation("plus", VariableReference(name_token.value), value),
        )

    def parse_subtract(self):
        self.advance()  # consume 'subtract'
        value = self.parse_expression()
        self.expect_word("from")
        name_token = self.expect(TokenType.WORD)
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return Assignment(
            name_token.value,
            BinaryOperation("minus", VariableReference(name_token.value), value),
        )

    def parse_multiply(self):
        self.advance()  # consume 'multiply'
        name_token = self.expect(TokenType.WORD)
        self.expect_word("by")
        value = self.parse_expression()
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return Assignment(
            name_token.value,
            BinaryOperation("times", VariableReference(name_token.value), value),
        )

    def parse_divide(self):
        self.advance()  # consume 'divide'
        name_token = self.expect(TokenType.WORD)
        self.expect_word("by")
        value = self.parse_expression()
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return Assignment(
            name_token.value,
            BinaryOperation("divided_by", VariableReference(name_token.value), value),
        )

    def parse_increase(self):
        self.advance()  # consume 'increase'
        name_token = self.expect(TokenType.WORD)
        self.expect_word("by")
        value = self.parse_expression()
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return Assignment(
            name_token.value,
            BinaryOperation("plus", VariableReference(name_token.value), value),
        )

    def parse_decrease(self):
        self.advance()  # consume 'decrease'
        name_token = self.expect(TokenType.WORD)
        self.expect_word("by")
        value = self.parse_expression()
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return Assignment(
            name_token.value,
            BinaryOperation("minus", VariableReference(name_token.value), value),
        )

    def parse_put(self):
        self.advance()  # consume 'put'
        element = self.parse_expression()
        self.expect_word("into")
        list_name = self.expect(TokenType.WORD)
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return ListAppend(list_name.value, element)

    def parse_remove(self):
        self.advance()  # consume 'remove'
        element = self.parse_expression()
        self.expect_word("from")
        list_name = self.expect(TokenType.WORD)
        if self.peek().type == TokenType.PERIOD:
            self.advance()
        return ListRemove(list_name.value, element)
