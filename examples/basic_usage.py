#!/usr/bin/env python3
"""Basic usage example for package_name.

This example demonstrates the most common usage patterns for the package.
"""

from package_name import __version__, get_logger, greet, setup_logging


def main() -> None:
    """Run basic usage examples."""
    # Display package version
    print(f"Using package_name version {__version__}")
    print()

    # Example 1: Basic operation
    print("Example 1: Basic Operation")
    print("-" * 40)

    # Use the greet function
    message = greet()
    print(f"Default greeting: {message}")

    custom_message = greet("Developer")
    print(f"Custom greeting:  {custom_message}")

    print("Basic operation completed successfully!")
    print()

    # Example 2: Working with data
    print("Example 2: Working with Data")
    print("-" * 40)
    data = {"key": "value", "count": 42}
    print(f"Input data: {data}")
    # Placeholder for future data processing capabilities
    print("Data processing is ready to be implemented.")
    print()

    # Example 3: Error handling
    print("Example 3: Error Handling")
    print("-" * 40)
    try:
        # Example of handling potential errors (if applicable)
        # result = might_fail()
        print("Operation succeeded!")
    except Exception as e:
        print(f"Caught exception: {e}")
    print()

    # Example 4: Logging
    print("Example 4: Basic Logging")
    print("-" * 40)
    # Setup simple console logging
    setup_logging(level="INFO")
    logger = get_logger(__name__)

    # Log some messages at different levels
    logger.info("This is an info message - appears in console")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    print("Check the console output above for log messages")
    print("For structured JSON logging, see examples/advanced_usage.py")
    print()

    print("All examples completed!")


if __name__ == "__main__":
    main()
