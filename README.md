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

[ ] Add comprehensive expenses.

[ ] Double check period with year argument

## Resources

Wouldn't be possible without [sec-api](https://github.com/janlukasschroeder/sec-api-python), hoping to make this totally independent and built in [Rust](https://github.com/TiesdeKok/fast_xbrl_parser/tree/master) eventually, though.

o [XBLR Guide](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf)
