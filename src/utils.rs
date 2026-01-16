use std::collections::HashMap;
use std::fs::File;
use std::io::BufReader;
use serde_json::Value;

// Load a JSON file into a HashMap
pub fn load_json(file_path: &str) -> Result<HashMap<String, Value>, Box<dyn std::error::Error>> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);
    let json: HashMap<String, Value> = serde_json::from_reader(reader)?;
    Ok(json)
}
