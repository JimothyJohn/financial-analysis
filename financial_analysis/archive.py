def get_gaap_period_dict(filing_category: dict, year: int) -> dict[str, int]:
    index: int = 0

    output: dict[str, int] = {}

    for index in range(len(filing_category)):
        if int(filing_category[index]["period"]["endDate"][:4]) != year:
            continue

        if "segment" in filing_category[index]:
            if "explicitMember" in filing_category[index]["segment"]:
                output[
                    get_value(
                        filing_category[index]["segment"]["explicitMember"], "dimension"
                    )
                ] = int(get_value(filing_category[index]))
            else:
                output[get_value(filing_category[index]["segment"], "dimension")] = int(
                    get_value(filing_category[index])
                )
        else:
            output["net"] = int(get_value(filing_category[index]))

    return output
