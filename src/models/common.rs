use serde_json::Value;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use log::{debug, info};
use chrono::{Datelike, NaiveDate};
use serde::de::Deserializer;

fn deserialize_from_str<'de, D, T>(deserializer: D) -> Result<T, D::Error>
where
    D: Deserializer<'de>,
    T: std::str::FromStr,
    T::Err: std::fmt::Display,
{
    let s: String = Deserialize::deserialize(deserializer)?;
    s.parse::<T>().map_err(serde::de::Error::custom)
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Period {
    #[serde(rename = "startDate")]
    pub start_date: NaiveDate,
    #[serde(rename = "endDate")]
    pub end_date: NaiveDate,
}

impl Default for Period {
    fn default() -> Self {
        Period {
            // Default to widely compatible epoch date
            start_date: NaiveDate::from_ymd_opt(1970, 1, 1).unwrap(),
            end_date: NaiveDate::from_ymd_opt(1970, 1, 1).unwrap(),
        }
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct MetricValue {
    #[serde(deserialize_with = "deserialize_from_str")]
    pub decimals: i8,
    #[serde(rename = "unitRef")]
    pub unit_ref: String,
    pub period: Period,
    #[serde(deserialize_with = "deserialize_from_str")]
    pub value: i64,
}

impl Default for MetricValue {
    fn default() -> Self {
        MetricValue {
            decimals: 0,
            unit_ref: String::from("usd"),
            period: Period::default(),
            value: 0,
        }
    }
}

impl MetricValue {
    pub fn new() -> Self {
        MetricValue {
            decimals: 0,
            unit_ref: String::from("usd"),
            period: Period::default(),
            value: 0,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Keywords {
    pub good: Vec<String>,
    pub bad: Vec<String>,
}

// set the initial value of net to 0 and the keywords to an empty list
impl Default for Keywords {
    fn default() -> Self {
        Keywords {
            good: vec![String::from("")],
            bad: vec![String::from("")],
        }
    }
}

impl Keywords {
    pub fn new(good: Vec<&str>, bad: Vec<&str>) -> Self {
        Keywords {
            good: good.iter().map(|s| s.to_string()).collect(),
            bad: bad.iter().map(|s| s.to_string()).collect(),
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Metric {
    pub net: MetricValue,
    pub breakdown: HashMap<String, MetricValue>,
    // #[serde(skip)]
    pub keywords: Keywords,
}

// set the initial value of net to 0 and the keywords to an empty list
impl Default for Metric {
    fn default() -> Self {
        Metric {
            net: MetricValue::default(),
            breakdown: HashMap::new(),
            keywords: Keywords::default(),
        }
    }
}

impl Metric {
    pub fn new(keywords: Keywords) -> Self {
        Metric {
            net: MetricValue::new(),
            breakdown: HashMap::new(),
            keywords: keywords,
        }
    }

    pub fn update(&mut self, key: &str, data: &Value) {
        
        // If period and decimals
        let mut initialized = false;
        // Check if the key matches any keyword
        for keyword in &self.keywords.bad {
            // Skip empty keywords to avoid matching everything if initialized with default
            if keyword.is_empty() {
                continue;
            }
            
            debug!("Checking if key '{}' contains BAD keyword '{}'", key, keyword);
            
            // Exit loop if any bad keyword is found
            if key.contains(keyword) {
                return;
            }
        }
        for keyword in &self.keywords.good {
            // Skip empty keywords to avoid matching everything if initialized with default
            if keyword.is_empty() {
                continue;
            }
            debug!("Checking if key '{}' contains GOOD keyword '{}'", key, keyword);
            // Extract value
            if key.contains(keyword) {
            if let Some(array) = data.as_array() {
                for item in array {
                    // Simple filter: avoid segments for now if possible, or just take everything
                    if item.get("segment").is_none() {
                        // Try to deserialize directly into MetricValue
                        if let Ok(metric_val) = serde_json::from_value::<MetricValue>(item.clone()) {
                            info!("Matched key '{}' with keyword '{}', adding {}", key, keyword, metric_val.value);
                            // Example: Check if the year matches expectation (e.g. 2025)
                            if metric_val.period.end_date.year() != 2025 {
                                continue;
                            }
                            // See if this could be done earlier
                            if !initialized {
                            self.net.period = metric_val.period.clone();
                            self.net.decimals = metric_val.decimals;
                            initialized = true;
                            }
                            self.net.value += metric_val.value;
                            
                            // Update to utilize a MetricValue
                            let val = metric_val.value;
                            self.breakdown.entry(key.to_string())
                                .and_modify(|e| e.value += val)
                                .or_insert(metric_val);
                        }
                    }
                }
            }
        }
            }
        }

    // add all of the breakdown values into the net value of Metric
    pub fn sum(&mut self) {
        for breakdown in &self.breakdown {
            self.net.value += breakdown.1.value;
        }
    }
}