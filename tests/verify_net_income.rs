use financial_analysis::models::finance::Income;
use financial_analysis::utils::load_json;

/// Runs the same statement-processing loop as `app::app` against a committed
/// fixture (AIT FY2025 10-K JSON as produced by the Python EDGAR parser), so
/// the pipeline is exercised in CI without network access or gitignored
/// `outputs/` artifacts. Expected values mirror the assertions in `src/app.rs`.
#[test]
fn verify_net_income_amounts() {
    financial_analysis::config::init("ait".to_string(), 2025);
    let json = load_json("tests/fixtures/ait_2025_10-K.json")
        .expect("Failed to read fixture. Run 'cargo test' from the project root.");

    let mut income = Income::default();
    for statement in ["StatementsOfIncome", "StatementsOfComprehensiveIncome"] {
        let map = json
            .get(statement)
            .and_then(|s| s.as_object())
            .unwrap_or_else(|| panic!("Fixture missing {statement}"));
        for (key, value) in map {
            income.update(key, value);
        }
    }

    assert_eq!(income.revenue.net.value, 4_563_424_000, "Revenue mismatch");
    assert_eq!(income.costs.net.value, -3_180_265_000, "Costs mismatch");
    assert_eq!(
        income.operations.net.value, -884_630_000,
        "Operations mismatch"
    );
    assert_eq!(income.expenses.net.value, 3_050_000, "Expenses mismatch");
    assert_eq!(
        income.investments.net.value, 17_602_000,
        "Investments mismatch"
    );
    assert_eq!(income.debt.net.value, -18_214_000, "Debt mismatch");
    assert_eq!(income.taxes.net.value, -107_979_000, "Taxes mismatch");
    assert_eq!(
        income.currency_exchange.net.value, -1_655_000,
        "Currency Exchange mismatch"
    );
    assert_eq!(income.benefits.net.value, -67_000, "Benefits mismatch");
    assert_eq!(
        income.reclassification.net.value, -16_481_000,
        "Reclassification mismatch"
    );
    assert_eq!(
        income.income_loss_tax.net.value, 4_083_000,
        "Income Loss Tax mismatch"
    );
    assert_eq!(
        income.gross_profit(),
        1_383_159_000,
        "Gross profit mismatch"
    );
    assert_eq!(income.ebitda(), 498_529_000, "EBITDA mismatch");
    assert_eq!(income.net_income(), 378_868_000, "Net income mismatch");
}
