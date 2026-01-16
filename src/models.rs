use serde_json::Value;

#[derive(Debug)]
pub struct Metric {
    pub net: i64,
    pub keywords: Vec<String>,
}

// set the initial value of net to 0 and the keywords to an empty list
impl Default for Metric {
    fn default() -> Self {
        Metric {
            net: 0,
            keywords: vec![String::from("")],
        }
    }
}

impl Metric {
    pub fn new(keywords: Vec<&str>) -> Self {
        Metric {
            net: 0,
            keywords: keywords.iter().map(|s| s.to_string()).collect(),
        }
    }

    pub fn update(&mut self, key: &str, data: &Value) {
        // Check if the key matches any keyword
        for keyword in &self.keywords {
            // Skip empty keywords to avoid matching everything if initialized with default
            if keyword.is_empty() {
                continue;
            }
            if key.contains(keyword) {
                 // Extract value
                 if let Some(array) = data.as_array() {
                     for item in array {
                         // Simple filter: avoid segments for now if possible, or just take everything
                         if item.get("segment").is_none() {
                             if let Some(val_str) = item.get("value").and_then(|v| v.as_str()) {
                                 if let Ok(val_num) = val_str.parse::<i64>() {
                                     self.net += val_num;
                                 }
                             }
                         }
                     }
                 }
            }
        }
    }
}

#[derive(Debug)]
pub struct Income {
    pub revenue: Metric,
    pub costs: Metric,
    pub gross_profit: Metric,
    pub operations: Metric,
    pub ebitda: Metric,
    pub expenses: Metric,
    pub investments: Metric,
    pub debt: Metric,
    pub taxes: Metric,
    pub currency_exchange: Metric,
    pub benefits: Metric,
    pub reclassification: Metric,
    pub income_loss_tax: Metric,
    pub net_income: Metric,
}

impl Income {
    pub fn update(&mut self, key: &str, data: &Value) {
        self.revenue.update(key, data);
        self.costs.update(key, data);
        self.gross_profit.update(key, data);
        self.operations.update(key, data);
        self.ebitda.update(key, data);
        self.expenses.update(key, data);
        self.investments.update(key, data);
        self.debt.update(key, data);
        self.taxes.update(key, data);
        self.currency_exchange.update(key, data);
        self.benefits.update(key, data);
        self.reclassification.update(key, data);
        self.income_loss_tax.update(key, data);
        self.net_income.update(key, data);
    }
}

impl Default for Income {
    fn default() -> Self {
        Income {
            revenue: Metric::new(vec!["Revenue"]),
            costs: Metric::new(vec!["CostOf"]),
            gross_profit: Metric::default(),
            operations: Metric::new(vec!["Administrative"]),
            ebitda: Metric::default(),
            expenses: Metric::new(vec!["Expense", "Depreciat", "Restructur"]),
            investments: Metric::new(vec!["Investment"]),
            debt: Metric::new(vec!["Interest", "Expense"]),
            taxes: Metric::new(vec!["Tax"]),
            currency_exchange: Metric::new(vec!["Currency"]),
            benefits: Metric::new(vec!["etirement"]),
            reclassification: Metric::new(vec!["lassification"]),
            income_loss_tax: Metric::new(vec!["IncomeLossTax"]),
            net_income: Metric::default(),
        }
    }
}