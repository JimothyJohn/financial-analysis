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
    pub fn gross_profit(&self) -> i64 {
        self.revenue.net.value + self.costs.net.value
    }
    pub fn ebitda(&self) -> i64 {
        self.gross_profit() + self.operations.net.value
    }
    pub fn net_income(&self) -> i64 {
        self.ebitda() + self.expenses.net.value + self.investments.net.value + self.debt.net.value + self.taxes.net.value + self.currency_exchange.net.value + self.benefits.net.value + self.reclassification.net.value + self.income_loss_tax.net.value
    }
}

impl Default for Income {
    fn default() -> Self {
        Income {
            revenue: Metric::new(Keywords::new(vec!["Revenue"], vec![]), true),
            costs: Metric::new(Keywords::new(vec!["CostOf"], vec![]), false),
            operations: Metric::new(Keywords::new(vec!["Administrative"], vec!["Tax"]), false),
            expenses: Metric::new(Keywords::new(vec!["Expense", "Depreciat", "Restructur"], vec!["Tax", "Administrative", "Interest", "Net", "OperatingExpenses"]), true),
            investments: Metric::new(Keywords::new(vec!["Investment", "Dividend"], vec!["Tax"]), true),
            debt: Metric::new(Keywords::new(vec!["Interest"], vec!["Tax", "Investment"]), false),
            taxes: Metric::new(Keywords::new(vec!["Tax"], vec!["Comprehensive", "Revenue", "Operations"]), false),
            currency_exchange: Metric::new(Keywords::new(vec!["Currency"], vec![]), false),
            benefits: Metric::new(Keywords::new(vec!["etirement"], vec![]), false),
            reclassification: Metric::new(Keywords::new(vec!["lassification"], vec!["Benefit"]), false),
            income_loss_tax: Metric::new(Keywords::new(vec!["IncomeLossTax"], vec![]), true),
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
            cash: Metric::new(Keywords::new(vec!["Cash"], vec![]), true),
            assets: Metric::new(Keywords::new(vec!["Assets", "Inventory"], vec![]), true),
            liabilities: Metric::new(Keywords::new(vec!["Liabilities"], vec![]), false),
            equity: Metric::new(Keywords::new(vec!["Equity", "Treasury"], vec![]), true),
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
