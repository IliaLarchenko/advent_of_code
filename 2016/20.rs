use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let mut intervals = contents
        .trim()
        .split('\n')
        .map(|s| {
            let mut parts = s.split('-');
            let start = parts.next().unwrap().parse::<u32>().unwrap();
            let end = parts.next().unwrap().parse::<u32>().unwrap();
            (start, end)
        })
        .collect::<Vec<(u32, u32)>>();

    intervals.sort();

    let mut i = 0;
    while i < intervals.len() - 1 {
        if intervals[i + 1].0 == 0 || intervals[i + 1].0 - 1 <= intervals[i].1 {
            intervals[i] = (intervals[i].0, intervals[i].1.max(intervals[i + 1].1));
            intervals.remove(i + 1);
        } else {
            i += 1;
        }
    }

    let ans1 = intervals[0].1 + 1;

    println!("Part 1 answer:");
    println!("{}", ans1);

    let mut ans2 = 0;
    for i in 0..intervals.len() - 1 {
        ans2 += intervals[i + 1].0 - intervals[i].1 - 1;
    }

    println!("Part 2 answer:");
    println!("{}", ans2);
}
