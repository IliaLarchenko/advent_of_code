use std::collections::HashMap;
use std::fs;

fn get_check_sum(name: &str) -> String {
    let mut letters = name.chars().collect::<Vec<char>>();
    letters.sort();
    let mut counts = HashMap::new();

    for c in letters {
        *counts.entry(c).or_insert(0) -= 1;
    }

    let mut counts = counts
        .iter()
        .map(|(c, n)| (n, c))
        .collect::<Vec<(&i32, &char)>>();
    counts.sort();

    let mut ans = String::new();
    for (_, c) in counts[0..5].iter() {
        ans = format!("{}{}", ans, c);
    }
    ans
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();
    let (mut ans1, mut ans2) = (0, 0);

    for line in &lines {
        let mut words = line.split('-').collect::<Vec<&str>>();
        let last = words.pop().unwrap();
        let last = last.split('[').collect::<Vec<&str>>();
        let (name, sector) = (words.join(""), last[0].parse::<i32>().unwrap());
        let checksum = last[1].replace("]", "");

        if get_check_sum(&name) == checksum {
            ans1 += sector;

            let mut name = name.chars().collect::<Vec<char>>();
            for c in &mut name {
                *c = char::from_u32((*c as u32 - 'a' as u32 + sector as u32) % 26 + 'a' as u32)
                    .unwrap();
            }
            if name.iter().collect::<String>() == "northpoleobjectstorage" {
                ans2 = sector;
            }
        }
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
