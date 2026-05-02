# Binance Futures Trading Bot

A backend trading bot project built using Python, FastAPI, and Binance Futures Testnet API.

This project supports both:

- CLI-based order execution
- REST API-based order execution

The system includes:
- input validation
- structured response formatting
- logging
- Binance Futures integration
- layered backend architecture

---

# Features

## CLI Layer
Place orders directly from terminal using command-line arguments.

Supported:
- Market Orders
- Limit Orders

---

## API Layer
Built using FastAPI.

Endpoints:
- POST `/order/market`
- POST `/order/limit`

Includes:
- request validation using Pydantic
- structured JSON responses
- HTTP exception handling

---

## Validation Layer
Custom validation for:
- symbol normalization
- BUY/SELL validation
- quantity validation
- limit price validation

---

## Logging
Application logs are stored in:

```bash
logs/app.log
