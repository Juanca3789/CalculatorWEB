"""Welcome to Reflex! self file outlines the steps to create a basic app."""

import math

import reflex as rx

from rxconfig import config


class State(rx.State):
    text_field = ""
    more_options = False
    def sum(self, operands: list[str]):
        accum = 0
        for operand in operands:
            accum += self.calculateString(operand)
        return accum

    def mult(self, operands: list[str]):
        accum = 1
        for operand in operands:
            accum *= self.calculateString(operand)
        return accum

    def res(self, operands: list[str]):
        accum = self.calculateString(operands[0])
        for i in range(1, len(operands)):
            accum -= self.calculateString(operands[i])
        return accum

    def div(self, operands: list[str]):
        accum = self.calculateString(operands[0])
        for i in range(1, len(operands)):
            accum /= self.calculateString(operands[i])
        return accum

    def exp(self, operands: list[str]):
        if len(operands) == 2:
            return pow(self.calculateString(operands[0]), self.calculateString(operands[1]))
        else:
            operands[len(operands) - 2] = str(pow(self.calculateString(operands[len(operands) - 2]), self.calculateString(operands[len(operands) - 1])))
            operands.pop()
            return self.exp(operands)

    def calculateString(self, operation: str):
        if operation.find("(") != -1:
            pastOP = ""
            for i in range(operation.find("(") + 1, operation.find(")")):
                pastOP += operation[i]
            newOP = str(self.calculateString(pastOP))
            newOP = operation.replace("(" + pastOP + ")", newOP)
            return self.calculateString(newOP)
        elif operation.find("sin") != -1:
            operation = operation.replace("sin", '')
            return math.sin(math.radians(self.calculateString(operation)))
        elif operation.find("cos") != -1:
            operation = operation.replace("cos", '')
            return math.cos(math.radians(self.calculateString(operation)))
        elif operation.find("tan") != -1:
            operation = operation.replace("tan", '')
            return math.tan(math.radians(self.calculateString(operation)))
        elif operation.find('ln') != -1:
            operation = operation.replace("ln", '')
            return math.log(self.calculateString(operation), math.e)
        elif operation.find('log') != -1:
            operation = operation.replace("log", '')
            return math.log10(self.calculateString(operation))
        elif operation.find('Abs') != -1:
            operation = operation.replace("Abs", '')
            return abs(self.calculateString(operation))
        elif operation.find("%") != -1:
            operation = operation.replace("%", '')
            return self.calculateString(operation) / 100
        elif operation.find("!") != -1:
            operation = operation.replace("!", '')
            return math.factorial(int(self.calculateString(operation)))
        elif operation.find("+") != -1 :
            sums = operation.split("+")
            return self.sum(sums)
        elif operation.find("-", 1) != -1:
            rests = operation.split("-")
            if operation.find("-") == 0:
                rests.pop(0)
                rests[0] = str(-1 * self.calculateString(rests[0]))
            return self.res(rests)
        elif operation.find("*") != -1:
            mults = operation.split("*")
            return self.mult(mults)
        elif operation.find("/") != -1:
            divs = operation.split("/")
            return self.div(divs)
        elif operation.find("^") != -1:
            exps = operation.split("^")
            return self.exp(exps)
        elif operation.find("π") != -1:
            return math.pi
        elif operation.find("e") != -1:
            return math.e
        else:
            return float(operation)
    
    def writeInLabel(self, char: str):
        self.text_field += char

    def deleteLastChar(self):
        if self.text_field != "":
            self.text_field = self.text_field[:-1]

    def deleteAllChar(self):
        self.text_field = ""

    def calculateResult(self):
        if self.text_field != "":
            result = self.calculateString(self.text_field)
            if result - int(result) == 0:
                result = int(result)
            self.text_field = str(result)
    
    def changeMoreOptions(self):
        self.more_options = not(self.more_options)

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.box(
    rx.center(
        rx.card(
            rx.center(
                rx.input(
                    read_only=True,
                    width="100%",
                    text_align="right",
                    value= State.text_field,
                    on_change= State.set_text_field
                ),
                rx.cond(
                    State.more_options,
                    rx.grid(
                        rx.button("AC", on_click= State.deleteAllChar()),
                        rx.button("DL", on_click= State.deleteLastChar()),
                        rx.button("√", on_click=State.writeInLabel("^(1/")),
                        rx.button("Deg", on_click=State.writeInLabel("/")),
                        rx.button("(", on_click=State.writeInLabel("(")),
                        rx.button(")", on_click=State.writeInLabel(")")),
                        rx.button("ln", on_click=State.writeInLabel("ln(")),
                        rx.button("Inv", on_click=State.writeInLabel("*")),
                        rx.button("sin", on_click=State.writeInLabel("sin(")),
                        rx.button("cos", on_click= State.writeInLabel("cos(")),
                        rx.button("log", on_click=State.writeInLabel("log(")),
                        rx.button("Abs", on_click=State.writeInLabel("Abs(")),
                        rx.button("tan", on_click=State.writeInLabel("tan(")),
                        rx.button("e", on_click=State.writeInLabel("e")),
                        rx.button("π", on_click=State.writeInLabel("π")),
                        rx.button("P", on_click=State.writeInLabel("P")),
                        rx.button("..", on_click=State.changeMoreOptions()),
                        rx.button("!", on_click=State.writeInLabel("!")),
                        rx.button("%", on_click=State.writeInLabel("%")),
                        rx.button("=", on_click= State.calculateResult()),
                        columns="4",
                        spacing="2",
                        width= "100%"
                    ),
                    rx.grid(
                        rx.button("AC", on_click= State.deleteAllChar()),
                        rx.button("DL", on_click= State.deleteLastChar()),
                        rx.button("^", on_click=State.writeInLabel("^")),
                        rx.button("/", on_click=State.writeInLabel("/")),
                        rx.button("7", on_click=State.writeInLabel("7")),
                        rx.button("8", on_click=State.writeInLabel("8")),
                        rx.button("9", on_click=State.writeInLabel("9")),
                        rx.button("*", on_click=State.writeInLabel("*")),
                        rx.button("4", on_click=State.writeInLabel("4")),
                        rx.button("5", on_click= State.writeInLabel("5")),
                        rx.button("6", on_click=State.writeInLabel("6")),
                        rx.button("-", on_click=State.writeInLabel("-")),
                        rx.button("1", on_click=State.writeInLabel("1")),
                        rx.button("2", on_click=State.writeInLabel("2")),
                        rx.button("3", on_click=State.writeInLabel("3")),
                        rx.button("+", on_click=State.writeInLabel("+")),
                        rx.button("..", on_click=State.changeMoreOptions()),
                        rx.button("0", on_click=State.writeInLabel("0")),
                        rx.button(".", on_click=State.writeInLabel(".")),
                        rx.button("=", on_click= State.calculateResult()),
                        columns="4",
                        spacing="2",
                        width= "100%"
                    )
                ),
                direction="column",
                spacing="2"
            )
        ),
        align="center",
        justify="center",
        width="100%",
        height="100%"
    ),
    background_color="var(--gray-3)",
    width="100%",
    height="100vh"
)


app = rx.App()
app.add_page(index)
