use clap::Parser;
use std::fs::File;
use std::io::{self, Read};

#[derive(Parser)]
#[command(name = "disk-image-inspector")]
#[command(about = "Analyze disk images, search strings, recover deleted files", long_about = None)]
struct Cli {
    #[arg(short, long)]
    image: String,

    #[arg(short, long)]
    search: Option<String>,
}

fn main() -> io::Result<()> {
    let cli = Cli::parse();

    println!("Opening disk image: {}", cli.image);
    let mut file = File::open(cli.image)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;

    println!("Image size: {} bytes", buffer.len());

    if let Some(keyword) = cli.search {
        println!("Searching for keyword: {}", keyword);
        let content = String::from_utf8_lossy(&buffer);
        for (idx, line) in content.lines().enumerate() {
            if line.contains(&keyword) {
                println!("Found in line {}: {}", idx + 1, line);
            }
        }
    }

    Ok(())
}
