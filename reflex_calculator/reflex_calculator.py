"""Welcome to Reflex! self file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    text_field = ""

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
        elif operation.find("+") != -1 :
            sums = operation.split("+")
            return self.sum(sums)
        elif operation.find("-", 1) != -1:
            rests = operation.split("-")
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
                rx.grid(
                    rx.button("CE", on_click= State.deleteAllChar()),
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
                    rx.button("0", on_click=State.writeInLabel("0")),
                    rx.button("00", on_click=State.writeInLabel("00")),
                    rx.button(".", on_click=State.writeInLabel(".")),
                    rx.button("=", on_click= State.calculateResult()),
                    columns="4",
                    spacing="2",
                    width= "100%"
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
