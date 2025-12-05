#!/usr/bin/env python3
"""Basic usage example for package_name.

This example demonstrates the most common usage patterns for the package.
"""

from package_name import __version__


def main():
    """Run basic usage examples."""
    # Display package version
    print(f"Using package_name version {__version__}")
    print()

    # Example 1: Basic operation
    print("Example 1: Basic Operation")
    print("-" * 40)
    # TODO: Add your basic usage example here
    # result = your_function()
    # print(f"Result: {result}")
    print("Basic operation completed successfully!")
    print()

    # Example 2: Working with data
    print("Example 2: Working with Data")
    print("-" * 40)
    data = {"key": "value", "count": 42}
    print(f"Input data: {data}")
    # TODO: Process data with your package
    # processed = process_data(data)
    # print(f"Processed: {processed}")
    print()

    # Example 3: Error handling
    print("Example 3: Error Handling")
    print("-" * 40)
    try:
        # TODO: Add code that might raise an exception
        # result = might_fail()
        print("Operation succeeded!")
    except Exception as e:
        print(f"Caught exception: {e}")
    print()

    print("All examples completed!")


if __name__ == "__main__":
    main()
