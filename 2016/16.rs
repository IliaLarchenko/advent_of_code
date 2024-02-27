use std::fs;

fn get_check_sum(s: &Vec<bool>) -> Vec<bool> {
    let mut result = Vec::new();
    let mut i = 0;
    while i < s.len() - 1 {
        if s[i] == s[i + 1] {
            result.push(true);
        } else {
            result.push(false);
        }
        i += 2;
    }

    if result.len() % 2 == 0 {
        return get_check_sum(&result);
    }

    result
}

fn get_zero(rot: usize) -> bool {
    let next_power = rot.next_power_of_two();
    if next_power == rot || rot == 0 {
        return false;
    } else {
        return !get_zero(next_power - rot);
    }
}

fn get_i(s: &Vec<bool>, i: usize) -> bool {
    let pos = i % (s.len() + 1);
    let rot = i / (s.len() + 1);
    if pos == s.len() {
        return get_zero(rot + 1);
    }
    if rot % 2 == 0 {
        return s[pos];
    } else {
        return !s[s.len() - pos - 1];
    }
}

fn get_first_checksum(s: &Vec<bool>, l: usize) -> Vec<bool> {
    let mut result = Vec::new();
    let mut i = 0;

    while i < l {
        let c1 = get_i(s, i);
        let c2 = get_i(s, i + 1);
        if c1 == c2 {
            result.push(true);
        } else {
            result.push(false);
        }
        i += 2;
    }

    result
}

fn vec_to_str(s: &Vec<bool>) -> String {
    let mut result = String::new();

    for c in s {
        if *c {
            result.push('1');
        } else {
            result.push('0');
        }
    }

    result
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let string = contents.trim().to_string();
    let mut s = Vec::new();

    for c in string.chars() {
        if c == '1' {
            s.push(true);
        } else {
            s.push(false);
        }
    }

    let checksum = get_first_checksum(&s, 272);
    let cs1 = get_check_sum(&checksum);
    let ans1 = vec_to_str(&cs1);

    println!("Part 1 answer:");
    println!("{}", ans1);

    let checksum2 = get_first_checksum(&s, 35651584);
    let cs2 = get_check_sum(&checksum2);
    let ans2 = vec_to_str(&cs2);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
