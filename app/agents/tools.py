from langchain_core.tools import tool
from typing import Optional


@tool
def get_current_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location.

    Args:
        location: The city and state, e.g., San Francisco, CA
        unit: The temperature unit to use (celsius or fahrenheit)
    """
    return f"The weather in {location} is sunny and 22°{unit[0].upper()}"


@tool
def search_web(query: str) -> str:
    """Search the web for information.

    Args:
        query: The search query
    """
    return f"Search results for: {query}. This is a mock search result."


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Args:
        expression: A mathematical expression to evaluate, e.g., "2 + 2"
    """
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"


def get_default_tools():
    """Return the default set of tools for the agent."""
    return [get_current_weather, search_web, calculate]