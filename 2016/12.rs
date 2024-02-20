use std::collections::HashMap;
use std::fs;

struct Instruction<'a> {
    name: &'a str,
    param1: &'a str,
    param2: &'a str,
}

fn run_instructions(instructions: &Vec<Instruction>, c: i32) -> i32 {
    let mut i = 0;
    let mut registers: HashMap<&str, i32> = HashMap::new();
    registers.insert("a", 0);
    registers.insert("b", 0);
    registers.insert("c", c);
    registers.insert("d", 0);

    'cycle: loop {
        if i >= instructions.len() {
            break 'cycle;
        }
        let inst = &instructions[i];
        match inst.name {
            "cpy" => {
                let val;
                if inst.param1 == "a"
                    || inst.param1 == "b"
                    || inst.param1 == "c"
                    || inst.param1 == "d"
                {
                    val = registers[inst.param1];
                } else {
                    val = inst.param1.parse::<i32>().unwrap();
                }
                registers.insert(inst.param2, val);
            }
            "inc" => {
                registers.insert(inst.param1, registers[inst.param1] + 1);
            }
            "dec" => {
                registers.insert(inst.param1, registers[inst.param1] - 1);
            }
            "jnz" => {
                let val;
                if inst.param1 == "a"
                    || inst.param1 == "b"
                    || inst.param1 == "c"
                    || inst.param1 == "d"
                {
                    val = registers[inst.param1];
                } else {
                    val = inst.param1.parse::<i32>().unwrap();
                }
                if val != 0 {
                    let new_i = i as i32 + inst.param2.parse::<i32>().unwrap();
                    i = new_i as usize;
                    continue 'cycle;
                }
            }
            _ => {
                println!("Error");
            }
        }
        i += 1;
    }
    return registers["a"];
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();
    let ans1;
    let ans2;
    let mut instructions: Vec<Instruction> = Vec::new();

    for line in lines {
        let words: Vec<&str> = line.split(" ").collect();
        let param1;
        let mut param2 = "";
        param1 = words[1];
        if words.len() > 2 {
            param2 = words[2];
        }
        instructions.push(Instruction {
            name: words[0],
            param1: param1,
            param2: param2,
        });
    }

    ans1 = run_instructions(&instructions, 0);

    println!("Part 1 answer:");
    println!("{}", ans1);

    ans2 = run_instructions(&instructions, 1);

    println!("Part 2 answer:");
    println!("{}", ans2);
}
