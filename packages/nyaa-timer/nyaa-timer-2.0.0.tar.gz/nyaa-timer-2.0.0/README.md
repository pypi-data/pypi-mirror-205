Title: Nyaatimer - A Simple Python Timer Decorator with Rich Output

Description:

Nyaatimer is a lightweight Python package that provides a simple timer decorator for measuring the execution time of functions. The package uses the `perf_counter` function from the `time` module to accurately measure the time taken, and the `rich` library to display the results in a visually appealing format.

Features:

- Easy-to-use decorator for timing function execution.
- Accurate time measurement using `perf_counter`.
- Attractive output with `rich` library integration.
- Displays function name, arguments, and keyword arguments in the output.

Example Usage:

To use Nyaatimer, simply import the `nyaatimer` decorator and apply it to any function you want to measure the execution time of:

```
from nyaatimer import nyaatimer


@nyaatimer
def example_function(a, b):
    return a + b


result = example_function(1, 2)
```

This will output the execution time and function details in a visually appealing format:

`Function example_function took 0.00012345 seconds Args=(1, 2), Kwargs={}`

Installation:

To install Nyaatimer, simply run the following command:

`pip install nyaatimer`

Requirements:

- Python 3.6 or later
- rich library (automatically installed as a dependency)

License:

Nyaatimer is released under the MIT License.
