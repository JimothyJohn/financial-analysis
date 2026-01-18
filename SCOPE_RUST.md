# Scope of Project

This project ingests SEC filings, specifically 10-K's, in JSON format and serializes then summarizes the financial data.

## Language

The language of choice is Rust. This is due to it's performance (which is honestly unnecessary for this scale of project) and progammability. It was previous built in Python, see [financial_anlaysis/](financial_anlaysis/). 

## Reference Material

The Python project in [financial_anlaysis/](financial_anlaysis/) can be used as reference as to what mostly needs to be done. The 10-K example JSON files are in [outputs/2025](outputs/2025).

## Readability

The code should be easily:

- Readable
- Understandable
- Debuggable
- Maintable
- Formatted
- Tested
- Scalable

## Implementation

All functions should have a corresponding test in the same file as the program as per I understand Rust best practice.

## Guidance

Frequently ask for feedback and do not create any code until you deeply understand what's wanted by the user.
