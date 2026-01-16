use crate::models::Income;
use crate::utils::load_json;

pub fn app() {
    let mut income = Income::default();
    let json = load_json("./outputs/2025/ait_10-k.json").expect("Unable to load JSON");
    
    // Access the nested income statement structure
    for statement in ["StatementsOfIncome", "StatementsOfComprehensiveIncome"] {
        if let Some(income_statement) = json.get(statement) {
            if let Some(map) = income_statement.as_object() {
                for (key, value) in map {
                    income.update(key, value);
                }
        }
    } else {
        println!("Could not find StatementsOfIncome");
    }

    println!("Final Income Statement: {:#?}", income);
}
}
