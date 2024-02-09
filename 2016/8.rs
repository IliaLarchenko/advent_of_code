use std::fs;

fn apply_step(name: &str, params: &str, rect: &mut Vec<Vec<i32>>) {
    if name == "rect" {
        let ab: Vec<&str> = params.split("x").collect();
        let a = ab[0].parse::<usize>().unwrap();
        let b = ab[1].parse::<usize>().unwrap();
        for i in 0..a {
            for j in 0..b {
                rect[j][i] = 1;
            }
        }
    } else if name == "rotate" {
        let split_param: Vec<&str> = params.split(" ").collect();
        let dir = split_param[0];
        let a = split_param[1].split("=").collect::<Vec<&str>>()[1]
            .parse::<usize>()
            .unwrap();
        let b = split_param[3].parse::<usize>().unwrap();

        if dir == "row" {
            let mut new_row = vec![0; 50];
            for i in 0..50 {
                new_row[(i + b) % 50] = rect[a][i];
            }
            rect[a] = new_row;
        } else if dir == "column" {
            let mut new_col = vec![0; 6];
            for i in 0..6 {
                new_col[(i + b) % 6] = rect[i][a];
            }
            for i in 0..6 {
                rect[i][a] = new_col[i];
            }
        }
    }
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();
    let mut ans1 = 0;
    let mut rect = vec![vec![0; 50]; 6];

    for line in &lines {
        let split_line: Vec<&str> = line.split(" ").collect();
        let name = split_line[0];
        let params = split_line[1..].join(" ");
        apply_step(name, &params, &mut rect);
    }

    for i in 0..6 {
        for j in 0..50 {
            ans1 += rect[i][j];
        }
    }

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    for i in 0..6 {
        for j in 0..50 {
            if rect[i][j] == 1 {
                print!("0");
            } else {
                print!(" ");
            }
        }
        println!("");
    }
}
