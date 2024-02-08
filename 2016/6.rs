use std::collections::HashMap;
use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();

    let mut counters = vec![
        HashMap::new(),
        HashMap::new(),
        HashMap::new(),
        HashMap::new(),
        HashMap::new(),
        HashMap::new(),
        HashMap::new(),
        HashMap::new(),
    ];
    let mut ans1 = String::new();
    let mut ans2 = String::new();

    for line in &lines {
        for (i, c) in line.chars().enumerate() {
            let counter = &mut counters[i];
            *counter.entry(c).or_insert(0) += 1;
        }
    }

    for i in 0..8 {
        let counter = &counters[i];
        let mut max = 0;
        let mut max_char = ' ';

        let mut min = std::usize::MAX;
        let mut min_char = ' ';

        for (c, count) in counter {
            if count > &max {
                max = *count;
                max_char = *c;
            }
            if count < &min {
                min = *count;
                min_char = *c;
            }
        }
        ans1 = format!("{}{}", ans1, max_char);
        ans2 = format!("{}{}", ans2, min_char);
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
