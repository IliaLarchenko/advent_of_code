use std::collections::HashMap;
use std::fs;

fn get_adjacent(x: i32, y: i32) -> Vec<(i32, i32)> {
    let mut result = Vec::new();
    if x > 0 {
        result.push((x - 1, y));
    }
    if y > 0 {
        result.push((x, y - 1));
    }
    result.push((x + 1, y));
    result.push((x, y + 1));
    result
}

fn get_position(x: i32, y: i32, favorite_number: i32, map: &mut HashMap<(i32, i32), bool>) -> bool {
    if map.contains_key(&(x, y)) {
        return false;
    }
    let mut sum = x * x + 3 * x + 2 * x * y + y + y * y + favorite_number;
    let mut count = 0;
    while sum > 0 {
        count += sum & 1;
        sum >>= 1;
    }
    if count % 2 == 0 {
        map.insert((x, y), true);
        return true;
    }
    map.insert((x, y), false);
    false
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let favorite_number: i32 = contents.trim().parse().unwrap();
    let mut ans1 = 0;
    let mut ans2 = 0;
    let mut map = HashMap::new();

    let mut queue = Vec::new();

    queue.push((1, 1, 0));
    map.insert((1, 1), true);
    while !queue.is_empty() {
        let (x, y, steps) = queue.remove(0);
        if x == 31 && y == 39 {
            ans1 = steps;
            break;
        }
        for (nx, ny) in get_adjacent(x, y) {
            if get_position(nx, ny, favorite_number, &mut map) {
                queue.push((nx, ny, steps + 1));
            }
        }
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    let mut map = HashMap::new();
    let mut queue = Vec::new();
    queue.push((1, 1, 0));
    map.insert((1, 1), true);

    while !queue.is_empty() {
        let (x, y, steps) = queue.remove(0);
        ans2 += 1;
        for (nx, ny) in get_adjacent(x, y) {
            if get_position(nx, ny, favorite_number, &mut map) {
                if steps < 50 {
                    queue.push((nx, ny, steps + 1));
                }
            }
        }
    }

    println!("Part 2 answer:");
    println!("{}", ans2);
}
