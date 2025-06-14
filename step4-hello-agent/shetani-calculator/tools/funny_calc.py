import random
from agents import function_tool

@function_tool
def add(a: float, b:float)-> str:
    """Add two numbers with fun twist. However, must mention fun_score in final_output"""
    fun_score = random.randint(1,5)
    return f"{a} + {b} = {a+b+fun_score} (Fun Score added = {fun_score})"

@function_tool
def substract(a:float, b:float)-> str:
    """Substract two numbers with fun twist. However, must mention fun_score in final_output"""
    fun_score = random.randint(1, 5)
    return f"{a} - {b} = {a - b + fun_score} (Fun Score added = {fun_score})"

@function_tool
def multiply(a:float, b:float)-> str:
    """Multiply two numbers with fun twist. However, must mention fun_score in final_output"""
    fun_score = random.randint(1, 5)
    return f"{a} x {b} = {(a * b) + fun_score} (Fun Score added = {fun_score})"

@function_tool
def divide(a:float, b:float)-> str:
    """Divide two numbers with fun twist. However, must mention fun_score in final_output"""
    fun_score = random.randint(1, 5)
    return f"{a} / {b} = {(a / b) + fun_score} (Fun Score added = {fun_score})"