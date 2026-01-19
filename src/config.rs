use std::sync::OnceLock;

#[derive(Debug)]
pub struct Config {
    pub company: String,
    pub year: i32,
}

static CONFIG: OnceLock<Config> = OnceLock::new();

pub fn init(company: String, year: i32) {
    CONFIG.get_or_init(|| Config { company, year });
}

pub fn get() -> &'static Config {
    CONFIG.get().expect("Config is not initialized")
}
