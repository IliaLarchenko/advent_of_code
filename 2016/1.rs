use std::collections::HashSet;
use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");

    let mut direction = 0;
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut step;
    let mut visited = HashSet::new();
    let mut ans2 = -1;

    for part in contents.trim().split(", ") {
        if part.chars().nth(0).unwrap() == 'R' {
            direction = (direction + 1) % 4;
        } else {
            direction = (direction + 3) % 4;
        }
        step = part[1..].parse::<i32>().unwrap();

        match direction {
            0 => {
                y += step;
                for i in 0..step {
                    if !visited.insert((x, y - i)) && ans2 == -1 {
                        ans2 = x.abs() + (y - i).abs();
                    }
                }
            }
            1 => {
                x += step;
                for i in 0..step {
                    if !visited.insert((x - i, y)) && ans2 == -1 {
                        ans2 = (x - i).abs() + y.abs();
                    }
                }
            }
            2 => {
                y -= step;
                for i in 0..step {
                    if !visited.insert((x, y + i)) && ans2 == -1 {
                        ans2 = x.abs() + (y + i).abs();
                    }
                }
            }
            3 => {
                x -= step;
                for i in 0..step {
                    if !visited.insert((x + i, y)) && ans2 == -1 {
                        ans2 = (x + i).abs() + y.abs();
                    }
                }
            }
            _ => println!("Error"),
        }
    }

    println!("Part 1 answer:");
    println!("{}", x.abs() + y.abs());

    println!("Part 2 answer:");
    println!("{}", ans2);
}
