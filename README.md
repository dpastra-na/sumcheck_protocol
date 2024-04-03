# sumcheck_protocol

Didactic implementation of the sumcheck protocol over finite fields.

Based on [J. Thaler, Proofs, Arguments, and Zero-Knowledge, 2023](https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.pdf).

## Structure

- `field.py` -- Finite field arithmetic (F_p)
- `polynomial.py` -- Multivariate polynomials over F_p
- `sumcheck.py` -- Prover, Verifier, and protocol orchestration
- `main.py` -- Executable example with Thaler's polynomial

## Setup

```bash
uv sync
```

## Usage

```bash
uv run python main.py
```

## Development

```bash
make test      # run tests
make lint      # run ruff check
make format    # auto-format
make check     # lint + tests
```
