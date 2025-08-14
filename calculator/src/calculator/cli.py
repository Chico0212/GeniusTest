import typer
from typing import Annotated
from .calculator import Calculator

app = typer.Typer(help="A simple calculator CLI application")

state = {"calc": Calculator()}


@app.command()
def add(
    a: Annotated[float, typer.Argument(help="First number")],
    b: Annotated[float, typer.Argument(help="Second number")]
):
    """Add two numbers"""
    result = state["calc"].add(a, b)
    typer.echo(f"Result: {result}")

@app.command()
def subtract(
    a: Annotated[float, typer.Argument(help="First number")],
    b: Annotated[float, typer.Argument(help="Second number")]
):
    """Subtract second number from first number"""
    result = state["calc"].subtract(a, b)
    typer.echo(f"Result: {result}")


@app.command()
def multiply(
    a: Annotated[float, typer.Argument(help="First number")],
    b: Annotated[float, typer.Argument(help="Second number")]
):
    """Multiply two numbers"""
    result = state["calc"].multiply(a, b)
    typer.echo(f"Result: {result}")


@app.command()
def divide(
    a: Annotated[float, typer.Argument(help="First number")],
    b: Annotated[float, typer.Argument(help="Second number")]
):
    """Divide first number by second number"""
    try:
        result = state["calc"].divide(a, b)
        typer.echo(f"Result: {result}")
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def power(
    a: Annotated[float, typer.Argument(help="Base number")],
    b: Annotated[float, typer.Argument(help="Exponent")]
):
    """Raise first number to the power of second number"""
    result = state["calc"].power(a, b)
    typer.echo(f"Result: {result}")


@app.command()
def history():
    """Show calculation history"""
    history = state["calc"].get_history()
    if not history:
        typer.echo("No calculations in history")
    else:
        typer.echo("Calculation History:")
        for calculation in history:
            typer.echo(f"  {calculation}")


@app.command()
def clear():
    """Clear calculation history"""
    state["calc"].clear_history()
    typer.echo("History cleared")

if __name__ == "__main__":
    app()