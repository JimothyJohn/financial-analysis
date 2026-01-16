# Scope of Project

This project ingest SEC filings, specifically 10-K's as JSON and serializes and summarizes the financial data for analysis.

## Language

The language of choice is Rust. There should be no dependencies if possible, besides dev dependencies. 

## Reference Material

The Python project in [financial_anlaysis/](financial_anlaysis/) can be used as reference as to what mostly needs to be done. The 10-K example JSON files are in [outputs/2025](outputs/2025).

## Readability

The code should be readable and maintainable. The code should be easy to understand and follow. The code should be easy to debug and maintain. The code should be easy to scale and maintain.

## Implementation

All functions should have a referred test in the same file as the program as per I understand Rust best practice.

## Guidance

Frequently ask for feedback as you go along function by function and piece by piece.

## Fun

You are racing the user building the program in src/main.rs. Yours should be main-ai.rs so that they can be distignuished. You're welcome to create as many associated, modular files of independent or helpful functions that I could possible also utilize in my main.rs file.