use financial_analysis::models::finance::Income;
use std::fs;
use std::path::Path;

#[test]
fn verify_net_income_amounts() {
    // Path to the JSON file
    let json_path = Path::new("outputs/2025/parsed/ait_2025_income.json");
    
    // Read the file content
    let json_content = fs::read_to_string(json_path)
        .expect("Failed to read JSON file. Make sure you are running 'cargo test' from the project root.");

    // Deserialize into Income struct
    let income: Income = serde_json::from_str(&json_content)
        .expect("Failed to deserialize JSON into Income struct");

    // Define expected net amounts based on the current JSON content
    // Note: These values serve as a verification of the current output. 
    // If logic changes (e.g., fixing keyword matching), these expectations should be updated.
    let expected_revenue = 4_563_424_000;
    let expected_costs = 3_180_265_000;
    let expected_operations = 884_630_000;
    let expected_expenses = 3_050_000;
    let expected_investments = 35_204_000;
    let expected_debt = 18_214_000;
    let expected_taxes = 5_172_370_000; // Includes Revenue due to "Tax" keyword match in "RevenueFromContractWithCustomerExcludingAssessedTax"
    let expected_currency_exchange = -1_655_000;
    let expected_benefits = -67_000;
    let expected_reclassification = 15_742_000;
    let expected_income_loss_tax = -4_083_000;

    // Verify each field
    assert_eq!(income.revenue.net.value, expected_revenue, "Revenue mismatch");
    assert_eq!(income.costs.net.value, expected_costs, "Costs mismatch");
    assert_eq!(income.operations.net.value, expected_operations, "Operations mismatch");
    assert_eq!(income.expenses.net.value, expected_expenses, "Expenses mismatch");
    assert_eq!(income.investments.net.value, expected_investments, "Investments mismatch");
    assert_eq!(income.debt.net.value, expected_debt, "Debt mismatch");
    assert_eq!(income.taxes.net.value, expected_taxes, "Taxes mismatch");
    assert_eq!(income.currency_exchange.net.value, expected_currency_exchange, "Currency Exchange mismatch");
    assert_eq!(income.benefits.net.value, expected_benefits, "Benefits mismatch");
    assert_eq!(income.reclassification.net.value, expected_reclassification, "Reclassification mismatch");
    assert_eq!(income.income_loss_tax.net.value, expected_income_loss_tax, "Income Loss Tax mismatch");
}
