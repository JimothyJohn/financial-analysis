# Financial Analysis

This is a simple financial analysis tool that uses the SEC's EDGAR API to retrieve financial data for a given company.

## Quickstart (MacOS/Linux)

o [Get API Key](https://sec-api.io/signup/free)

o Reconfigure [.env.example](.env.example) and rename it to [.env](.env).

```bash
# Choose a company by stock symbol
./Quickstart aapl
```

## TODO

[ ] Consolidate expenses into lists of keys and summarize them.

[ ] Add comprehensive expenses.

[ ] Find better solution for deriving keys for each line item.

## Resources

Wouldn't be possible without sec-api, hoping to make totally independent and built in Rust eventually, though, would be cool.

o [XBLR to JSON](https://github.com/janlukasschroeder/sec-api-python?tab=readme-ov-file#xbrl-to-json-converter-api)

o [XBLR Guide](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf)

o [Rust XBLR Parser](https://github.com/TiesdeKok/fast_xbrl_parser/tree/master)
