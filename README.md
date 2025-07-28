# PrimeSieve

A Python project that efficiently generates and stores prime numbers
using bit arrays, designed to benchmark various algorithms and hardware performance.

---

## Table of Contents

- [Description](#description)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Testing](#testing)  
- [Benchmarks](#benchmarks)  
- [Contributing](#contributing)  
- [License](#license)  
- [Contact](#contact)

---

## Description

The codebase is organized into separate modules and classes, each responsible for distinct functionality.  
The main entry point of the project is `coordinator.py`.
The `file_manager.py` module handles file operations, while `prime_calculator.py` is responsible for computation.
Additional utility functions are located in `utils.py`.  

---

## Requirements

- Python 3.x  
- Dependencies listed in `requirements.txt`, including but not limited to:  
  - `bitarray`  
  - `pytest` (for testing)  
- It is recommended to use a virtual environment.

---

## Installation

1. Clone the repository:  
   ```bash
    git clone https://github.com/MarcinDJacz/primes
    cd primes

    Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

    Install dependencies:
    pip install -r requirements.txt

## Usage

Run the main program:
python coordinator.py

To execute tests:
pytest tests

Benchmarks are available in the [benchmarks] directory and can be run separately as needed.

## Project Structure

    coordinator.py — Main entry point orchestrating the program flow.

    file_manager.py — Handles file reading and writing operations.

    prime_calculator.py — Contains logic for prime number calculations.

    utils.py — Additional helper functions.

Directories:

    [benchmarks] — Contains performance benchmarks for various implementations and hardware measurements.

    [tests] — Contains unit and integration tests.

    [docs] — Documentation and conclusions from tests.

## Testing

To run the full test suite, use:

pytest tests

## Benchmarks

Performance tests can be found in the [benchmarks] directory. These assess different algorithmic approaches as well as hardware capabilities.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests. For bug reports or feature requests, use the issue tracker.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Author: Marcin Djaczuk
Email: marcindjaczuk@gmail.com
GitHub: https://github.com/MarcinDJacz/
