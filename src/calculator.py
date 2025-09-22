from sympy import sympify

def calculate_expression(expression):
    try:
        result = sympify(expression)
        return f"The result of {expression} is {result}."
    except Exception:
        return "I'm not sure how to respond to that."
