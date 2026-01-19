use crate::models::finance::Income;
use crate::utils::load_json;
use log::{info, warn, error};

// Create function with default year of 2025
pub fn app(symbol: String, year: i32) {
    let mut income = Income::default();
    let json_path = format!("./outputs/2025/{symbol}_10-k.json");
    
    info!("📂 Loading JSON from: {}", json_path);
    
    let json = match load_json(&json_path) {
        Ok(data) => {
            info!("✅ Successfully loaded JSON data");
            data
        },
        Err(e) => {
            error!("❌ Failed to load JSON: {}", e);
            return;
        }
    };
    
    // Access the nested income statement structure
    info!("🔍 Analyzing Income Statements...");
    for statement in ["StatementsOfIncome", "StatementsOfComprehensiveIncome"] {
        if let Some(income_statement) = json.get(statement) {
            info!("Found {}", statement);
            if let Some(map) = income_statement.as_object() {
                info!("📊 Processing {}", statement);
                for (key, value) in map {
                    income.update(key, value);
                }
            } else {
                warn!("⚠️ Could not find {}", statement);
            }
        } else {
            warn!("⚠️ Could not find {}", statement);
        }
    }
    
    let output_file = format!("outputs/2025/parsed/{}_{}_income.json", symbol, year);
    if let Some(parent) = std::path::Path::new(&output_file).parent() {
        std::fs::create_dir_all(parent).expect("Unable to create directory");
    }
    
    match std::fs::File::create(&output_file) {
        Ok(file) => {
            if let Err(e) = serde_json::to_writer_pretty(file, &income) {
                error!("❌ Failed to write JSON: {}", e);
            } else {
                info!("💾 Saved income statement to {}", output_file);
            }
        },
        Err(e) => error!("❌ Failed to create output file: {}", e),
    }

    match symbol == "ait" && year == 2025 {
        true => {
            // Assert this instead to save lines of code
            assert_eq!(income.revenue.net.value, 4563424000);
            assert_eq!(income.costs.net.value, -3180265000);
            assert_eq!(income.operations.net.value, -884630000);
            assert_eq!(income.expenses.net.value, 3050000);
            assert_eq!(income.investments.net.value, 17602000);
            assert_eq!(income.debt.net.value, -18214000);
            assert_eq!(income.taxes.net.value, -107979000);
            assert_eq!(income.currency_exchange.net.value, -1655000);
            assert_eq!(income.benefits.net.value, -67000);
            assert_eq!(income.reclassification.net.value, -16481000);
            assert_eq!(income.income_loss_tax.net.value, 4083000);
            assert_eq!(income.gross_profit(), 1383159000);
            assert_eq!(income.ebitda(), 498529000);
        }
        false => (),
    }
    println!("Net Income: {}", income.net_income());
}
