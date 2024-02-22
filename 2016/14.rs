use md5; // need to add md5 = "0.7.3" to Cargo.toml
use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;

fn find_all_repeat(s: &str, n: usize) -> Vec<char> {
    let mut ans = Vec::new();
    let mut i = 0;
    while i < s.len() {
        let mut j = i;
        while j < s.len() && s.chars().nth(i).unwrap() == s.chars().nth(j).unwrap() {
            j += 1;
        }
        if j - i >= n {
            ans.push(s.chars().nth(i).unwrap());
        }
        i = j;
    }
    ans
}

fn get_answer(salt: &str, stretch: bool) -> usize {
    let mut ans: usize = 0;
    let mut has_triple: HashMap<char, Vec<usize>> = HashMap::new();
    let mut answers = HashSet::new();
    let mut max_id = 0;

    'main_loop: for i in 0.. {
        let s = format!("{}{}", salt, i);
        let mut hash = format!("{:x}", md5::compute(s));
        if stretch {
            for _ in 0..2016 {
                hash = format!("{:x}", md5::compute(hash));
            }
        }
        let triples = find_all_repeat(&hash, 3);
        let fives = find_all_repeat(&hash, 5);

        if triples.len() > 0 {
            if has_triple.contains_key(&triples[0]) {
                let mut ids: Vec<usize>;
                ids = has_triple.get_mut(&triples[0]).unwrap().to_vec();
                ids.push(i);
                has_triple.insert(triples[0], ids);
            } else {
                has_triple.insert(triples[0], vec![i]);
            }
        }

        for c in fives {
            if let Some(ids) = has_triple.get(&c) {
                for id in ids {
                    if i - *id <= 1000 && i != *id {
                        answers.insert(*id);
                        if answers.len() == 64 {
                            max_id = *id + 1000;
                        }
                    }
                }
            }
        }

        if max_id > 0 && i == max_id {
            let mut v: Vec<usize> = answers.into_iter().collect();
            v.sort();
            ans = v[63];
            break 'main_loop;
        }
    }
    ans
}

fn main() {
    let salt = fs::read_to_string("input.txt").expect("Error");
    let ans1;
    let ans2;

    ans1 = get_answer(&salt, false);

    println!("Part 1 answer:");
    println!("{}", ans1);

    ans2 = get_answer(&salt, true);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
