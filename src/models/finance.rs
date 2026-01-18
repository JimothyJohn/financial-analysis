use serde::{Deserialize, Serialize};
use serde_json::Value;
use crate::models::common::{Metric, Keywords};


#[derive(Debug, Serialize, Deserialize)]
pub struct Income {
    pub revenue: Metric,
    pub costs: Metric,
    pub operations: Metric,
    pub expenses: Metric,
    pub investments: Metric,
    pub debt: Metric,
    pub taxes: Metric,
    pub currency_exchange: Metric,
    pub benefits: Metric,
    pub reclassification: Metric,
    pub income_loss_tax: Metric,
}

impl Income {
    pub fn update(&mut self, key: &str, data: &Value) {
        self.revenue.update(key, data);
        self.costs.update(key, data);
        self.operations.update(key, data);
        self.expenses.update(key, data);
        self.investments.update(key, data);
        self.debt.update(key, data);
        self.taxes.update(key, data);
        self.currency_exchange.update(key, data);
        self.benefits.update(key, data);
        self.reclassification.update(key, data);
        self.income_loss_tax.update(key, data);
    }
}

impl Default for Income {
    fn default() -> Self {
        Income {
            revenue: Metric::new(Keywords::new(vec!["Revenue"], vec![])),
            costs: Metric::new(Keywords::new(vec!["CostOf"], vec![])),
            operations: Metric::new(Keywords::new(vec!["Administrative"], vec!["Tax"])),
            expenses: Metric::new(Keywords::new(vec!["Expense", "Depreciat", "Restructur"], vec!["Tax", "Administrative", "Interest", "Net"])),
            investments: Metric::new(Keywords::new(vec!["Investment", "Dividend"], vec!["Tax"])),
            debt: Metric::new(Keywords::new(vec!["Interest"], vec!["Tax", "Investment"])),
            taxes: Metric::new(Keywords::new(vec!["Tax"], vec!["Comprehensive"])),
            currency_exchange: Metric::new(Keywords::new(vec!["Currency"], vec![])),
            benefits: Metric::new(Keywords::new(vec!["etirement"], vec![])),
            reclassification: Metric::new(Keywords::new(vec!["lassification"], vec![])),
            income_loss_tax: Metric::new(Keywords::new(vec!["IncomeLossTax"], vec![])),
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BalanceSheet {
    pub cash: Metric,
    pub assets: Metric,
    pub liabilities: Metric,
    pub equity: Metric,
}

impl Default for BalanceSheet {
    fn default() -> Self {
        BalanceSheet {
            cash: Metric::new(Keywords::new(vec!["Cash"], vec![])),
            assets: Metric::new(Keywords::new(vec!["Assets", "Inventory"], vec![])),
            liabilities: Metric::new(Keywords::new(vec!["Liabilities"], vec![])),
            equity: Metric::new(Keywords::new(vec!["Equity", "Treasury"], vec![])),
        }
    }
}

impl BalanceSheet {
    pub fn update(&mut self, key: &str, data: &Value) {
        self.cash.update(key, data);
        self.assets.update(key, data);
        self.liabilities.update(key, data);
        self.equity.update(key, data);
    }
}
