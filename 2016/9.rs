use std::fs;

fn decode_marker(s: &str) -> (usize, usize) {
    if s.contains("x") {
        let nums: Vec<&str> = s.split("x").collect();
        if nums.len() == 2 {
            let l = nums[0].parse::<usize>().unwrap();
            let r = nums[1].parse::<usize>().unwrap();
            return (l, r);
        }
    }
    return (0, 0);
}

fn compute_len(s: &str, recursive: bool) -> usize {
    let mut ans = 0;
    let mut i = 0;
    let chars = s.chars().collect::<Vec<char>>();
    let mut marker: (usize, usize);
    let mut open = chars.len();

    while i < chars.len() {
        if chars[i] == '(' {
            open = i;
        } else if chars[i] == ')' {
            if open < i {
                marker = decode_marker(&chars[open + 1..i].iter().collect::<String>());
                if recursive {
                    ans += compute_len(
                        &chars[i + 1..i + 1 + marker.0].iter().collect::<String>(),
                        true,
                    ) * marker.1;
                } else {
                    ans += marker.0 * marker.1;
                }
                ans -= i - open - 1;
                i += 1 + marker.0;
                open = chars.len();
                continue;
            }
        } else if chars[i] != ' ' {
            ans += 1;
        }
        i += 1;
    }
    return ans;
}

fn main() {
    let content = fs::read_to_string("input.txt").expect("Error");

    let ans1 = compute_len(&content, false);

    println!("Part 1 answer:");
    println!("{}", ans1);

    let ans2 = compute_len(&content, true);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
