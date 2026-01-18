use clap::Parser;
use src::app::app;

use log::info;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    /// Company symbol
    #[arg(short, long)]
    company: String,

    /// Year of the report
    #[arg(short, long, default_value_t = 2025)]
    year: i32,
}

fn main() {
    env_logger::builder()
        .format_timestamp(Some(env_logger::TimestampPrecision::Seconds))
        .filter_level(log::LevelFilter::Info)
        .init();

    let args = Args::parse();
    info!("🚀 Starting Financial Analysis for {} ({})", args.company, args.year);
    
    app(args.company, args.year);

    info!("🏁 Analysis Complete");
} 
