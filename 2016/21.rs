use std::fs;

fn apply_op(pass: &mut Vec<char>, op: &Vec<&str>, reverse: bool) {
    match op[0] {
        "swap" => match op[1] {
            "position" => {
                let x = op[2].parse::<usize>().unwrap();
                let y = op[5].parse::<usize>().unwrap();
                pass.swap(x, y);
            }
            "letter" => {
                let x = pass
                    .iter()
                    .position(|&c| c == op[2].chars().next().unwrap())
                    .unwrap();
                let y = pass
                    .iter()
                    .position(|&c| c == op[5].chars().next().unwrap())
                    .unwrap();
                pass.swap(x, y);
            }
            _ => {}
        },
        "rotate" => match op[1] {
            "left" => {
                let x = op[2].parse::<usize>().unwrap();
                if reverse {
                    pass.rotate_right(x);
                } else {
                    pass.rotate_left(x);
                }
            }
            "right" => {
                let x = op[2].parse::<usize>().unwrap();
                if reverse {
                    pass.rotate_left(x);
                } else {
                    pass.rotate_right(x);
                }
            }
            "based" => {
                let mut x = pass
                    .iter()
                    .position(|&c| c == op[6].chars().next().unwrap())
                    .unwrap();
                if reverse {
                    if x == 0 {
                        x += pass.len();
                    }
                    if x % 2 == 0 {
                        x = (x + pass.len() - 2) / 2;
                    } else {
                        x = (x - 1) / 2;
                    }
                }
                let x = if x >= 4 { x + 2 } else { x + 1 };
                let x = x % pass.len();
                if reverse {
                    pass.rotate_left(x);
                } else {
                    pass.rotate_right(x);
                }
            }
            _ => {}
        },
        "reverse" => {
            let x = op[2].parse::<usize>().unwrap();
            let y = op[4].parse::<usize>().unwrap();
            pass[x..=y].reverse();
        }
        "move" => {
            let x = op[2].parse::<usize>().unwrap();
            let y = op[5].parse::<usize>().unwrap();
            if reverse {
                let c = pass.remove(y);
                pass.insert(x, c);
            } else {
                let c = pass.remove(x);
                pass.insert(y, c);
            }
        }
        _ => {}
    }
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let mut operations = contents
        .trim()
        .split('\n')
        .map(|s| s.split(' ').collect::<Vec<&str>>())
        .collect::<Vec<Vec<&str>>>();

    let mut pass: Vec<char> = "abcdefgh".chars().collect();

    for op in &operations {
        apply_op(&mut pass, &op, false);
        apply_op(&mut pass, &op, true);
        if pass.iter().collect::<String>() != "abcdefgh" {
            println!("{:?} ", op);
        }
    }

    for op in &operations {
        apply_op(&mut pass, &op, false);
    }

    let ans1 = pass.iter().collect::<String>();

    println!("Part 1 answer:");
    println!("{}", ans1);

    let mut pass: Vec<char> = "fbgdceah".chars().collect();
    operations.reverse();

    // Test of reverse operations
    // Can be ignored
    for op in &operations {
        apply_op(&mut pass, &op, false);
        apply_op(&mut pass, &op, true);
        if pass.iter().collect::<String>() != "fbgdceah" {
            println!("{:?} ", op);
        }
    }

    for op in &operations {
        apply_op(&mut pass, &op, true);
    }

    let ans2 = pass.iter().collect::<String>();

    println!("Part 2 answer:");
    println!("{}", ans2);
}
