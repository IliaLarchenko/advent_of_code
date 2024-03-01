use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let num = contents.trim().parse::<usize>().unwrap();

    let mut elves = Vec::new();
    elves.push((num - 1, 1));
    for i in 1..num - 1 {
        elves.push((i - 1, i + 1));
    }
    elves.push((num - 2, 0));

    let mut i = 0;
    while elves[i].0 != elves[i].1 {
        let (prev, next) = elves[i];
        let new_next = elves[next].1;
        elves[i] = (prev, new_next);
        elves[new_next] = (i, elves[new_next].1);
        i = new_next;
    }

    let ans1 = i + 1;

    println!("Part 1 answer:");
    println!("{}", ans1);

    let mut last_win = 0;
    for n in 2..num + 1 {
        last_win += 1;
        if last_win >= n / 2 {
            last_win += 1;
        }
        last_win %= n;
    }

    let ans2 = last_win + 1;

    println!("Part 2 answer:");
    println!("{}", ans2);
}
