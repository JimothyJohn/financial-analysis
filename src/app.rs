use crate::models::finance::Income;
use crate::utils::load_json;
use log::{info, warn, error};

// Create function with default year of 2025
pub fn app(symbol: String, year: i32) {
    let mut income = Income::default();
    let json_path = format!("./outputs/{year}/{symbol}_10-k.json");
    
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
}
