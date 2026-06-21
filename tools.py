import datetime

def calculator(expression: str) -> str:
    """
    Evaluates a simple mathematical expression.
    
    Args:
        expression: The math expression to evaluate (e.g., '2 + 2', '10 * 5').
    """
    try:
        # In a real app, use a safer eval or a dedicated parser.
        # For this example, we use eval with restricted globals.
        allowed_names = {"+": None, "-": None, "*": None, "/": None, "%": None}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

def get_current_time(timezone: str = "UTC") -> str:
    """
    Returns the current time.
    
    Args:
        timezone: The timezone to get the time for (e.g., 'UTC').
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    return f"Current time ({timezone}): {now.isoformat()}"

def run_code(code: str) -> str:
    """
    Executes Python code.
    
    Args:
        code: The Python code to execute.
    """
    return "Code execution is disabled in this environment. Please just output the python code as text to the user."

# List of tools to pass to Gemini
gemini_tools = [calculator, get_current_time, run_code]
