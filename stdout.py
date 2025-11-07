"""
Utility module for file naming and output management
"""

import os
from datetime import datetime


def smartFilename(base_filename, add_timestamp=False, output_dir='output'):
    """
    Generate a smart filename with optional timestamp and directory management.

    Parameters:
    -----------
    base_filename : str
        The base filename (e.g., 'data.csv')
    add_timestamp : bool, optional
        Whether to add timestamp to filename (default: False)
    output_dir : str, optional
        Output directory path (default: 'output')

    Returns:
    --------
    str : Full path to the file

    Examples:
    ---------
    >>> smartFilename('data.csv')
    'output/data.csv'

    >>> smartFilename('data.csv', add_timestamp=True)
    'output/data_20240101_123456.csv'
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if add_timestamp:
        # Split filename and extension
        name, ext = os.path.splitext(base_filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}{ext}"
    else:
        filename = base_filename

    return os.path.join(output_dir, filename)


def print_section(title, width=80, char='='):
    """
    Print a formatted section header.

    Parameters:
    -----------
    title : str
        Section title
    width : int, optional
        Width of the separator line (default: 80)
    char : str, optional
        Character to use for separator (default: '=')
    """
    print(f"\n{char * width}")
    print(f"{title:^{width}}")
    print(f"{char * width}\n")


if __name__ == '__main__':
    # Test the functions
    print("Testing smartFilename...")
    print(smartFilename('test.csv'))
    print(smartFilename('test.csv', add_timestamp=True))

    print_section("Test Section")
