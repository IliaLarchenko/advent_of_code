use std::fs;

#[derive(Clone)]
struct Bot {
    low: i32,
    high: i32,
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();
    let mut ans1: i32 = -1;
    let ans2;
    let mut output: Vec<i32> = vec![-1; 300];
    let mut bots: Vec<Bot> = vec![Bot { low: -1, high: -1 }; 300];

    for line in &lines {
        let words: Vec<&str> = line.split(" ").collect();
        if words[0] == "value" {
            let value = words[1].parse::<i32>().unwrap();
            let bot_id = words[5].parse::<usize>().unwrap();
            if bots[bot_id].low == -1 {
                bots[bot_id].low = value;
            } else {
                if bots[bot_id].low > value {
                    bots[bot_id].high = bots[bot_id].low;
                    bots[bot_id].low = value;
                } else {
                    bots[bot_id].high = value;
                }
            }
        }
    }

    'outer_loop: loop {
        for line in &lines {
            let words: Vec<&str> = line.split(" ").collect();
            if words[0] == "bot" {
                let bot_id1 = words[1].parse::<usize>().unwrap();
                let bot_id_low = words[6].parse::<usize>().unwrap();
                let bot_id_high = words[11].parse::<usize>().unwrap();

                if bots[bot_id1].low != -1 && bots[bot_id1].high != -1 {
                    if bots[bot_id1].low == 17 && bots[bot_id1].high == 61 {
                        ans1 = bot_id1.clone() as i32;
                    }
                    let type_low = words[5];
                    let type_high = words[10];

                    for (bot_id2, value, output_type) in [
                        (bot_id_low, bots[bot_id1].low, type_low),
                        (bot_id_high, bots[bot_id1].high, type_high),
                    ]
                    .iter()
                    {
                        if *output_type == "bot" {
                            if bots[*bot_id2].low == -1 {
                                bots[*bot_id2].low = *value;
                            } else {
                                if bots[*bot_id2].low > *value {
                                    bots[*bot_id2].high = bots[*bot_id2].low;
                                    bots[*bot_id2].low = *value;
                                } else {
                                    bots[*bot_id2].high = *value;
                                }
                            }
                        } else {
                            output[*bot_id2] = *value;
                        }
                    }
                    if output[0] != -1 && output[1] != -1 && output[2] != -1 && ans1 >= 0 {
                        ans2 = output[0] * output[1] * output[2];
                        break 'outer_loop;
                    }
                    bots[bot_id1].low = -1;
                    bots[bot_id1].high = -1;
                }
            }
        }
    }
    println!("Part 1 answer:");
    println!("{}", ans1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
