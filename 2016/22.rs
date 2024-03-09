use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let mut df = contents.trim().split('\n').collect::<Vec<&str>>();
    df.remove(0);
    df.remove(0);
    let mut max_x = 0;
    let mut max_y = 0;
    let mut disks = vec![];

    for i in df {
        let mut parts = i.split(' ');
        let mut num = parts.next().unwrap().split('-').collect::<Vec<&str>>();
        let y = num.pop().unwrap()[1..].parse::<usize>().unwrap();
        let x = num.pop().unwrap()[1..].parse::<usize>().unwrap();
        max_x = max_x.max(x);
        max_y = max_y.max(y);
        let mut size = parts.next().unwrap();
        while size == "" {
            size = parts.next().unwrap();
        }
        let size = size[..size.len() - 1].parse::<usize>().unwrap();
        let mut used = parts.next().unwrap();
        while used == "" {
            used = parts.next().unwrap();
        }
        let used = used[..used.len() - 1].parse::<usize>().unwrap();
        disks.push((x, y, size, used));
    }

    let mut ans1 = 0;

    for i in 0..disks.len() {
        for j in 0..disks.len() {
            if i != j && disks[i].3 != 0 && disks[i].3 <= disks[j].2 - disks[j].3 {
                ans1 += 1;
            }
        }
    }

    // Need for visualization
    let mut grid = vec![vec!['.'; max_x + 1]; max_y + 1];

    let mut empty_x = 0;
    let mut empty_y = 0;
    let mut wall_x = max_x;

    for d in disks {
        if d.2 > 100 {
            grid[d.1][d.0] = '#';
            wall_x = wall_x.min(d.0);
        } else if d.2 - d.3 > 75 {
            grid[d.1][d.0] = '_';
            empty_x = d.0;
            empty_y = d.1;
        } else {
            grid[d.1][d.0] = '.';
        }
    }
    grid[0][max_x] = 'G';
    println!(
        "{}",
        grid.iter()
            .map(|x| x.iter().collect::<String>())
            .collect::<Vec<String>>()
            .join("\n")
    );

    let ans2 = empty_y + 2 * (empty_x - wall_x + 1) + (max_x - empty_x) + 5 * (max_x - 1);

    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
