use std::fs;

fn is_triangle(sides: &Vec<i32>) -> i32 {
    if sides[0] + sides[1] > sides[2]
        && sides[0] + sides[2] > sides[1]
        && sides[1] + sides[2] > sides[0]
    {
        1
    } else {
        0
    }
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();

    let mut ans1 = 0;
    let mut ans2 = 0;
    let mut columns: Vec<Vec<i32>> = vec![vec![], vec![], vec![]];

    for line in &lines {
        let sides: Vec<i32> = line
            .split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
        ans1 += is_triangle(&sides);

        for (i, side) in sides.iter().enumerate() {
            columns[i].push(*side);
        }

        if columns[0].len() == 3 {
            for i in 0..3 {
                ans2 += is_triangle(&columns[i]);
            }
            columns = vec![vec![], vec![], vec![]];
        }
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
