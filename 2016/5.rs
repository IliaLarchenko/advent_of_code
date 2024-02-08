use md5;
use std::fs; // need to add md5 = "0.7.3" to Cargo.toml

fn main() {
    let doorid = fs::read_to_string("input.txt").expect("Error");
    let mut ans1 = String::new();
    let mut ans2 = vec![' '; 8];

    'main_loop: for i in 0.. {
        let s = format!("{}{}", doorid, i);
        let hash = md5::compute(s);
        let hash = format!("{:x}", hash);

        if i % 100000 == 0 {
            println!("{}", i);
        }

        if hash.chars().take(5).collect::<String>() == "00000" {
            println!("{}", hash);
            if ans1.to_string().len() < 8 {
                ans1 = format!("{}{}", ans1, hash.chars().nth(5).unwrap());
            }

            let pos = hash.chars().nth(5).unwrap();
            if !pos.is_digit(10) {
                continue;
            }
            let pos = pos.to_digit(10).unwrap() as usize;
            if pos > 7 {
                continue;
            }

            if ans2[pos] != ' ' {
                continue;
            }

            let val = hash.chars().nth(6).unwrap();
            ans2[pos] = val;

            if ans2.iter().all(|&c| c != ' ') {
                break 'main_loop;
            }
        }
    }

    let ans2: String = ans2.iter().collect();

    println!("{}", doorid);

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
