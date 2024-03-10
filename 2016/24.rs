use std::collections::HashMap;
use std::collections::HashSet;
use std::fs;

fn dijkstra(grid: &Vec<Vec<char>>, start: (usize, usize), end: (usize, usize)) -> usize {
    let mut queue1 = HashSet::new();
    let mut queue2 = HashSet::new();

    let mut steps = 0;

    queue1.insert(start);
    queue2.insert(end);

    loop {
        if queue1.len() > queue2.len() {
            let temp = queue1.clone();
            queue1 = queue2.clone();
            queue2 = temp;
        }
        let mut new_queue = HashSet::new();

        for (i, j) in queue1 {
            if queue2.contains(&(i, j)) {
                return steps;
            }
            for (x, y) in [(0, 1), (0, -1), (1, 0), (-1, 0)].iter() {
                let new_i = i as i32 + x;
                let new_j = j as i32 + y;
                if new_i >= 0
                    && new_i < grid.len() as i32
                    && new_j >= 0
                    && new_j < grid[0].len() as i32
                {
                    if grid[new_i as usize][new_j as usize] != '#' {
                        new_queue.insert((new_i as usize, new_j as usize));
                    }
                }
            }
        }
        queue1 = new_queue;
        steps += 1;
    }
}

fn min_distance(
    distances: &HashMap<(usize, usize), usize>,
    points: &Vec<(usize, usize)>,
    start: usize,
    visited: HashSet<usize>,
    ret: bool,
) -> usize {
    if visited.len() == points.len() {
        if ret {
            return distances[&(start, 0)];
        }
        return 0;
    }
    let mut min_dist = usize::MAX;
    for i in 0..points.len() {
        if visited.contains(&i) {
            continue;
        }
        let mut new_visited = visited.clone();
        new_visited.insert(i);
        let dist = distances[&(start, i)] + min_distance(distances, points, i, new_visited, ret);
        if dist < min_dist {
            min_dist = dist;
        }
    }
    return min_dist;
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();
    let mut grid = vec![vec!['.'; 178]; 45];
    let mut start = 0;
    let mut points = Vec::new();
    let mut distances = HashMap::new();

    for (i, line) in lines.iter().enumerate() {
        for (j, c) in line.chars().enumerate() {
            grid[i][j] = c;
            if c != '#' && c != '.' {
                points.push((i, j));
                if c == '0' {
                    start = points.len() - 1;
                }
            }
        }
    }

    for i in 0..points.len() {
        for j in i + 1..points.len() {
            let dist = dijkstra(&grid, points[i], points[j]);
            distances.insert((i, j), dist);
            distances.insert((j, i), dist);
        }
    }

    let mut visited = HashSet::new();
    visited.insert(start);
    let ans1 = min_distance(&distances, &points, start, visited, false);

    println!("Part 1 answer:");
    println!("{}", ans1);

    let mut visited = HashSet::new();
    visited.insert(start);
    let ans2 = min_distance(&distances, &points, start, visited, true);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
