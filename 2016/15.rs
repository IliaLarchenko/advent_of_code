use std::fs;

fn get_time(positions: &Vec<usize>, initial: &Vec<usize>) -> usize {
    let mut step = 1;
    let mut time = 0;
    let mut disc = 0;

    while disc < positions.len() {
        if (initial[disc] + time + disc + 1) % positions[disc] == 0 {
            disc += 1;
            step *= positions[disc - 1];
        } else {
            time += step;
        }
    }

    time
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");

    let mut positions = Vec::new();
    let mut initial = Vec::new();

    for line in contents.lines() {
        let data: Vec<&str> = line[..line.len() - 1].split_whitespace().collect();
        let pos = data[3].parse::<usize>().unwrap();
        let start = data[11].parse::<usize>().unwrap();

        positions.push(pos);
        initial.push(start);
    }

    let ans1 = get_time(&positions, &initial);

    println!("Part 1 answer:");
    println!("{}", ans1);

    positions.push(11);
    initial.push(0);

    let ans2 = get_time(&positions, &initial);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
