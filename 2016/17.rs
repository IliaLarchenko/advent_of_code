use md5; // need to add md5 = "0.7.3" to Cargo.toml
use std::collections::VecDeque as VecDeq;
use std::fs;

fn main() {
    let salt = fs::read_to_string("input.txt").expect("Error");
    let string = salt.trim().to_string();
    let mut queue = VecDeq::new();
    let mut ans1 = String::new();
    let mut ans2 = 0;

    queue.push_back((0, 0, string.clone()));

    loop {
        if queue.is_empty() {
            break;
        }
        let (x, y, s) = queue.pop_front().unwrap();
        if x == 3 && y == 3 {
            if ans1.is_empty() {
                ans1 = s[string.len()..].to_string();
            }
            ans2 = s.len() - string.len();
        } else {
            let hash = md5::compute(s.clone());
            let hash = format!("{:x}", hash);
            let hash = hash.chars().take(4).collect::<String>();
            let hash = hash
                .chars()
                .map(|c| "bcdef".contains(c))
                .collect::<Vec<bool>>();
            if y > 0 && hash[0] {
                queue.push_back((x, y - 1, s.clone() + "U"));
            }
            if y < 3 && hash[1] {
                queue.push_back((x, y + 1, s.clone() + "D"));
            }
            if x > 0 && hash[2] {
                queue.push_back((x - 1, y, s.clone() + "L"));
            }
            if x < 3 && hash[3] {
                queue.push_back((x + 1, y, s.clone() + "R"));
            }
        }
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
