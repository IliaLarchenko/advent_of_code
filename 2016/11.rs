use std::collections::HashSet;
use std::fs;

fn check_state(state: &Vec<usize>) -> bool {
    for i in state.len() / 2..state.len() - 1 {
        if (state[i] != state[i - state.len() / 2])
            && (state[..state.len() / 2].contains(&state[i]))
        {
            return false;
        }
    }
    true
}

fn generate_all_next_states(
    queue: &mut HashSet<Vec<usize>>,
    visited: &mut HashSet<Vec<usize>>,
) -> HashSet<Vec<usize>> {
    let mut new_queue = HashSet::new();

    for state in queue.iter() {
        let floor = state[state.len() - 1];
        let mut can_move = vec![];
        for i in 0..state.len() {
            if state[i] == floor {
                can_move.push(i);
            }
        }

        for i in 0..can_move.len() - 1 {
            for j in i + 1..can_move.len() {
                if floor < 3 {
                    let mut new_state = state.clone();
                    new_state[can_move[i]] += 1;
                    if j != can_move.len() - 1 {
                        new_state[can_move[j]] += 1;
                    }
                    new_state[state.len() - 1] += 1;
                    if check_state(&new_state) && !visited.contains(&new_state) {
                        new_queue.insert(new_state.clone());
                        visited.insert(new_state.clone());
                    }
                }
                if floor > 0 {
                    let mut new_state = state.clone();
                    new_state[can_move[i]] -= 1;
                    if j != can_move.len() - 1 {
                        new_state[can_move[j]] -= 1;
                    }
                    new_state[state.len() - 1] -= 1;
                    if check_state(&new_state) && !visited.contains(&new_state) {
                        new_queue.insert(new_state.clone());
                        visited.insert(new_state.clone());
                    }
                }
            }
        }
    }
    new_queue
}

fn djikstra(state: Vec<usize>) -> usize {
    let mut step = 0;
    let final_state = vec![3; state.len()];

    let mut queue1 = HashSet::new();
    let mut queue2 = HashSet::new();
    let mut visited1 = HashSet::new();
    let mut visited2 = HashSet::new();
    queue1.insert(state.clone());
    queue2.insert(final_state.clone());
    visited1.insert(state.clone());
    visited2.insert(final_state.clone());

    while queue1.len() > 0 && queue2.len() > 0 {
        if queue1.len() < queue2.len() {
            queue1 = generate_all_next_states(&mut queue1, &mut visited1);
        } else {
            queue2 = generate_all_next_states(&mut queue2, &mut visited2);
        }
        step += 1;

        for state in queue1.iter() {
            if queue2.contains(state) {
                return step;
            }
        }
    }
    0
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();
    let ans1;
    let ans2;
    let mut generators = vec![vec![]; 4];
    let mut microchips = vec![vec![]; 4];
    let mut names = vec![];

    for (i, line) in lines.iter().enumerate() {
        let line = line.replace(" and ", " ");
        let line = line.replace(" a ", " ");
        let line = line.replace(",", "");
        let line = line.replace(".", "");
        let words: Vec<&str> = line.split(" ").collect();

        for j in 2..words.len() {
            let word = words[j];
            if word == "generator" {
                generators[i].push(words[j - 1].to_string());
                names.push(words[j - 1].to_string());
            } else if word == "microchip" {
                microchips[i].push(words[j - 1].split("-").collect::<Vec<&str>>()[0].to_string());
            }
        }
    }

    let mut state = vec![0; names.len() * 2 + 1];
    for (i, floor) in generators.iter().enumerate() {
        for item in floor.iter() {
            let pos = names.iter().position(|x| x == item).unwrap();
            state[pos] = i;
        }
        for item in microchips[i].iter() {
            let pos = names.iter().position(|x| x == item).unwrap();
            state[pos + names.len()] = i;
        }
    }

    ans1 = djikstra(state.clone());

    println!("Part 1 answer:");
    println!("{}", ans1);

    let extra = 2;
    let mut new_state = vec![0; names.len() * 2 + 1 + extra * 2];
    for i in 0..names.len() {
        new_state[i] = state[i];
        new_state[i + names.len() + extra] = state[i + names.len()];
    }

    ans2 = djikstra(new_state.clone());

    println!("Part 2 answer:");
    println!("{}", ans2);
}
