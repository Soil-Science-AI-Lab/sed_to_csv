# Contributing to sed_to_csv

Thank you for your interest in contributing! Here's how to get started.

## Getting Started

1. **Fork** the repository and clone your fork:

   ```bash
   git clone https://github.com/<your-username>/sed_to_csv.git
   cd sed_to_csv
   ```

2. **Create a virtual environment** and install the package in editable mode:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Create a feature branch** off `main`:

   ```bash
   git checkout -b feature/your-improvement
   ```

## Making Changes

- Keep pull requests focused on a single change.
- Follow existing code style (PEP 8, type hints, docstrings).
- Add or update tests in `tests/` for any functional change.
- Run the test suite locally before submitting:

  ```bash
  pytest
  ```

## Submitting a Pull Request

1. Push your branch and open a PR against `main`.
2. Describe what changed and why.
3. Ensure all CI checks pass.

## Reporting Issues

Please open an issue on GitHub with:

- A clear description of the problem.
- Steps to reproduce (including sample `.sed` file if possible).
- Expected vs. actual behaviour.

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
