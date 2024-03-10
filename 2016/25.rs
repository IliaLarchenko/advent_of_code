use std::collections::HashMap;
use std::fs;

struct Instruction<'a> {
    name: &'a str,
    param1: &'a str,
    param2: &'a str,
}

fn detect_mult(instructions: &Vec<Instruction>, i: usize) -> bool {
    if i + 5 >= instructions.len() {
        return false;
    }
    if instructions[i].name == "cpy"
        && instructions[i + 1].name == "inc"
        && instructions[i + 2].name == "dec"
        && instructions[i + 3].name == "jnz"
        && instructions[i + 4].name == "dec"
        && instructions[i + 5].name == "jnz"
    {
        if instructions[i + 3].param2 == "-2" && instructions[i + 5].param2 == "-5" {
            return true;
        }
    }
    return false;
}

fn run_instructions(instructions: &mut Vec<Instruction>, a: i32) -> bool {
    let mut counter = 0;
    let mut i = 0;
    let mut registers: HashMap<&str, i32> = HashMap::new();
    registers.insert("a", a);
    registers.insert("b", 0);
    registers.insert("c", 0);
    registers.insert("d", 0);

    'cycle: for _ in 0..100000 {
        if i >= instructions.len() {
            break 'cycle;
        }
        let inst = &instructions[i];
        match inst.name {
            "cpy" => {
                if detect_mult(instructions, i) {
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

                    let var1 = inst.param2;
                    let var2 = instructions[i + 4].param1;
                    let target = instructions[i + 1].param1;

                    registers.insert(target, val * registers[var2] + registers[target]);
                    registers.insert(var1, 0);
                    registers.insert(var2, 0);
                    i += 6;
                    continue 'cycle;
                }
                if inst.param2 != "a"
                    && inst.param2 != "b"
                    && inst.param2 != "c"
                    && inst.param2 != "d"
                {
                    i += 1;
                    continue 'cycle;
                }
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
                let steps;
                if inst.param2 == "a"
                    || inst.param2 == "b"
                    || inst.param2 == "c"
                    || inst.param2 == "d"
                {
                    steps = registers[inst.param2];
                } else {
                    steps = inst.param2.parse::<i32>().unwrap();
                }
                if val != 0 {
                    let new_i = i as i32 + steps;
                    i = new_i as usize;
                    continue 'cycle;
                }
            }
            "out" => {
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
                if val != counter % 2 {
                    return false;
                }
                counter += 1;
                if counter > 10 {
                    return true;
                }
            }
            _ => {
                println!("Error");
            }
        }
        i += 1;
    }
    return false;
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("Error");
    let lines: Vec<&str> = contents.split("\n").collect();
    let mut ans1 = 0;
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

    let mut i = 0;
    while ans1 == 0 {
        if run_instructions(&mut instructions, i) {
            ans1 = i;
        }
        i += 1;
    }

    println!("Part 1 answer:");
    println!("{}", ans1);
}
