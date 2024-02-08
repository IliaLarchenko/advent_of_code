use std::fs;

fn check_abba(s: &str) -> bool {
    let mut abba = false;
    for i in 0..s.len() - 3 {
        let a = s.chars().nth(i).unwrap();
        let b = s.chars().nth(i + 1).unwrap();
        let c = s.chars().nth(i + 2).unwrap();
        let d = s.chars().nth(i + 3).unwrap();
        if a == d && b == c && a != b {
            abba = true;
        }
    }
    abba
}

fn find_all_aba(s: &str, reverse: bool, abas: &mut Vec<String>) {
    for i in 0..s.len() - 2 {
        let a = s.chars().nth(i).unwrap();
        let b = s.chars().nth(i + 1).unwrap();
        let c = s.chars().nth(i + 2).unwrap();
        if a == c && a != b {
            if reverse {
                abas.push(format!("{}{}{}", c, b, a));
            } else {
                abas.push(format!("{}{}{}", a, b, c));
            }
        }
    }
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();
    let mut ans1 = 0;
    let mut ans2 = 0;

    for line in &lines {
        let mut last = 0;
        let mut abba = false;
        let mut hypernet = true;

        let mut abas = Vec::new();
        let mut babs = Vec::new();

        for (mut i, c) in line.chars().enumerate() {
            if c == '[' || c == ']' || i == line.len() - 1 {
                if i == line.len() - 1 {
                    i += 1;
                }

                let s = &line[last..i];
                if c == ']' {
                    if check_abba(s) {
                        hypernet = false;
                    }
                    find_all_aba(s, true, &mut babs);
                } else {
                    if check_abba(s) {
                        abba = true;
                    }
                    find_all_aba(s, false, &mut abas);
                }
                last = i + 1;
            }
        }
        if abba && hypernet {
            ans1 += 1;
        }

        for aba in &abas {
            let bab = format!(
                "{}{}{}",
                &aba.chars().nth(1).unwrap(),
                &aba.chars().nth(0).unwrap(),
                &aba.chars().nth(1).unwrap()
            );
            if babs.contains(&bab) {
                ans2 += 1;
                break;
            }
        }
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
