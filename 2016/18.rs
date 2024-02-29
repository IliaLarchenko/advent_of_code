use std::fs;

fn get_next_string(string: &str) -> String {
    let mut new_string = String::new();
    let chars = string.chars().collect::<Vec<char>>();
    for i in 0..chars.len() {
        let left = if i == 0 { '.' } else { chars[i - 1] };
        let right = if i == chars.len() - 1 {
            '.'
        } else {
            chars[i + 1]
        };
        if left != right {
            new_string.push('^');
        } else {
            new_string.push('.');
        }
    }
    new_string
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let start = contents.trim().to_string();
    let mut string = start.clone();
    let mut ans1 = 0;
    let mut ans2 = 0;

    // We are probably supposed to find a cycle here, but it's not necessary
    // It takes ~2 seconds to calculate the answer
    for i in 0..400000 {
        ans2 += string.chars().filter(|&c| c == '.').count();
        string = get_next_string(&string);
        if i == 39 {
            ans1 = ans2;
        }
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
