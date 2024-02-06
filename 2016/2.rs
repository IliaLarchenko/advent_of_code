use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();

    let mut x = 1;
    let mut y = 1;
    let mut ans1 = String::new();
    let keypad1 = vec!["123", "456", "789"];

    for line in &lines {
        for c in line.chars() {
            match c {
                'U' => {
                    if y > 0 {
                        y -= 1
                    }
                }
                'D' => {
                    if y < 2 {
                        y += 1
                    }
                }
                'L' => {
                    if x > 0 {
                        x -= 1
                    }
                }
                'R' => {
                    if x < 2 {
                        x += 1
                    }
                }
                _ => break,
            }
        }
        ans1 = format!("{}{}", ans1, keypad1[y].chars().nth(x).expect("Error"));
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    let mut x = 0;
    let mut y = 2;
    let mut ans2 = String::new();
    let keypad2 = vec!["  1  ", " 234 ", "56789", " ABC ", "  D  "];

    for line in &lines {
        for c in line.chars() {
            match c {
                'U' => {
                    if y > 0 && keypad2[y - 1].chars().nth(x).unwrap() != ' ' {
                        y -= 1
                    }
                }
                'D' => {
                    if y < 4 && keypad2[y + 1].chars().nth(x).unwrap() != ' ' {
                        y += 1
                    }
                }
                'L' => {
                    if x > 0 && keypad2[y].chars().nth(x - 1).unwrap() != ' ' {
                        x -= 1
                    }
                }
                'R' => {
                    if x < 4 && keypad2[y].chars().nth(x + 1).unwrap() != ' ' {
                        x += 1
                    }
                }
                _ => break,
            }
        }
        ans2 = format!("{}{}", ans2, keypad2[y].chars().nth(x).expect("Error"));
    }

    println!("Part 2 answer:");
    println!("{}", ans2);
}
