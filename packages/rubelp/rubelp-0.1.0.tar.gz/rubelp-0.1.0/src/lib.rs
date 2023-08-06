mod tree;
mod node;

use std::collections::HashMap;
use std::iter::zip;
use pyo3::prelude::*;
use crate::tree::Tree;
use crate::node::Node;


enum TokenizeState{
    Word,
    Spunc,
    Wpunc,
    Space
}



/// tokenize(txt: str)
/// --
/// 
/// Fonction de tokenisation utilisant un transducteur à états finis.
/// 
/// :param txt: la chaîne de caractères à tokeniser
/// :type txt: str
#[pyfunction]
fn tokenize(txt: &str) -> PyResult<Vec<String>>{

    let mut tokens:Vec<String> = Vec::<String>::new();
    let mut buffer:String = String::new();

    let mut state:TokenizeState = TokenizeState::Space;

    for c in txt.chars()
    {
        match c{
            c if c.is_alphanumeric()=>{
                // Si le caractère est un élément de mot :

                match state{
                    TokenizeState::Word=>{
                        buffer.push(c);
                    },
                    TokenizeState::Spunc=>{
                        tokens.push(buffer.clone());
                        buffer.clear();
                        buffer.push(c);
                    },
                    TokenizeState::Wpunc=>{
                        buffer.push(c);
                    },
                    TokenizeState::Space=>{
                        buffer.push(c);
                    }
                }

                state = TokenizeState::Word;
                
            },
            c if c.is_whitespace()=>{
                // Si le caractère est un espace blanc :

                match state{
                    TokenizeState::Word=>{
                        tokens.push(buffer.clone());
                        buffer.clear();
                    },
                    TokenizeState::Spunc=>{
                        tokens.push(buffer.clone());
                        buffer.clear();
                    },
                    TokenizeState::Wpunc=>{},
                    TokenizeState::Space=>{}
                }

                state = TokenizeState::Space;
            },
            c if ['\'', '’'].contains(&c)=>{

                match state{
                    TokenizeState::Word=>{
                        buffer.push(c);
                        tokens.push(buffer.clone());
                        buffer.clear();
                    },
                    TokenizeState::Spunc=>{
                        tokens.push(buffer.clone());
                        buffer.clear();
                        buffer.push(c);
                    },
                    TokenizeState::Wpunc=>{
                        buffer.push(c);
                    },
                    TokenizeState::Space=>{
                        buffer.push(c);
                    }
                }

                state = TokenizeState::Wpunc;
            },
            c if [',', ';', ':', '–', '“', '”', '«', '»'].contains(&c)=>{

                match state{
                    TokenizeState::Word=>{
                        tokens.push(buffer.clone());
                        buffer.clear();
                        tokens.push(c.to_string());
                    },
                    TokenizeState::Spunc=>{
                        tokens.push(buffer.clone());
                        buffer.clear();
                        tokens.push(c.to_string());
                    },
                    TokenizeState::Wpunc=>{
                        tokens.push(c.to_string());
                    },
                    TokenizeState::Space=>{
                        tokens.push(c.to_string());
                    }
                }

                state = TokenizeState::Wpunc;
            },
            c if ['.', '?', '!'].contains(&c)=>{

                match state{
                    TokenizeState::Word=>{
                        tokens.push(buffer.clone());
                        buffer.clear();
                        buffer.push(c);
                    },
                    TokenizeState::Spunc=>{
                        buffer.push(c);
                    },
                    TokenizeState::Wpunc=>{
                        tokens.push(buffer.clone());
                        buffer.clear();
                        buffer.push(c);
                    },
                    TokenizeState::Space=>{
                        buffer.push(c);
                    }
                }

                state = TokenizeState::Spunc;
            },
            _=>buffer.push(c)
        }

    }

    return Ok(tokens);

}


fn split_rules(ruleset: HashMap<String, String>) -> (HashMap<String, String>, HashMap<String, String>, usize){

    let mut rules = HashMap::<String, String>::new();
    let mut split_rules = HashMap::<String, String>::new();
    let mut window = 1usize;

    for (key, value) in zip(ruleset.keys(), ruleset.values()){

        let len = key.clone().split("+").collect::<Vec<&str>>().len();

        if len > 1{
            split_rules.insert(key.to_string(), value.to_string());

            if len > window{
                window = len;
            }
        }
        else if len == 1{
            println!("{} : {}", key, value);
            rules.insert(key.to_string(), value.to_string());
        }
    }

    (rules, split_rules, window)
}


fn merge(ruleset: &HashMap<String, String>, array: Vec<&str>, window: usize) -> Vec<String>{

    let mut out = Vec::<String>::new();
    let mut offset = 0usize;


    for i in 0..array.len(){
        for size in (1..window).rev(){

            let lower = i+offset;
            let upper = i+offset+size;

            println!("lower : {} ; upper : {} ; len : {}", lower, upper, array.len());

            if upper <= array.len(){

                let merged: String = array[lower..upper].join("+");
                println!("{}", &merged);

                if ruleset.contains_key(&merged){
                    offset += size;
                    out.push(merged.clone());
                }

            }
            else{
                break;
            }

        }
    }

    out
}


/// engine(tokens: list[str], ruleset: dict)
/// --
/// 
/// Fonction faisant tourner le moteur à base de règles, à partir de tokens et d'un ensemble de règles.
/// 
/// :param tokens: la liste des tokens à traiter
/// :type tokens: list[str]
/// :param ruleset: la base de règles
/// :type ruleset: dict
/// :return: l'arbre résultant
/// :rtype: Tree
#[pyfunction]
fn engine(tokens: Vec<String>, ruleset: HashMap<String, String>) -> PyResult<Tree>{


    let (rules, split_rules, window) = split_rules(ruleset);

    // On initialise le premier niveau
    let mut previous_level = Vec::<Node>::new();
    
    let mut structure = Vec::<Vec<Node>>::new();

    let mut successful = true;
    let mut cmptr = 1usize;

    for (i, leaf) in tokens.iter().enumerate(){
        previous_level.push(Node::new(leaf.clone(), 0, i));
    }

    structure.push(previous_level.clone());


    while successful{

        successful = false;
        let mut previous_chunk = 0usize;

        let mut new_level = Vec::<Node>::new(); // On crée le nouveau niveau dans l'arborescence
        let mut index = 0;
    
        let vector = previous_level
            .iter()
            .map(|x| { // On applique les règles
                if rules.contains_key(&x.data) {rules.get(&x.data).unwrap()} 
                else {""}}) 
            .collect();
        let level: Vec<String> = merge(&split_rules, vector, window); // On récupère une liste des transformations

        println!("{:?}", level);
    
        for (i, ref item) in level.iter().enumerate(){ // Pour chaque élément, on vérifie s'il s'agit d'une transition :

            if item.to_owned() != "" && i > 0{ // Si la transformation a donné quelque chose et que l'on ne se trouve pas au début, alors on enregistre le chunk précédent

                let children: Vec<usize> = (previous_chunk..i).collect();
                let new_chunk = Node{data : level[children[0]].to_string(), index: index, level: cmptr, children : children};
    
                new_level.push(new_chunk);
                previous_chunk = i;
                index += 1;
                successful = true;
            }
        }

        // On s'assure de bien insérer le dernier chunk : 
        let children: Vec<usize> = (previous_chunk..level.len()).collect();
        let new_chunk = Node{
            data : if level.len() > 0 && children.len() > 0 {level[children[0]].to_string()} else {"0".to_string()}, 
            index: index, 
            level: cmptr, 
            children : children};
        new_level.push(new_chunk);

        previous_level = new_level.clone();

        // On n'ajoute de nouveau niveau que si celui-ci n'est pas vide
        if new_level.len() > 0{
            structure.push(new_level);
            cmptr += 1;
        }
        
    }


    Ok(Tree {data : structure})
}



/*
/// Moteur à base de règles simple. Il applique les règles données en entrée sur une liste de tokens (chaînes de caractères).
/// 
/// # Paramètres :
/// * `tokens` - la liste des tokens (liste python de chaînes de caractères)
/// * `ruleset` - dictionnaire de règles (dictionnaire python associant une chaîne à une autre chaîne)
#[pyfunction]
fn mbr_previous(tokens: Vec<String>, ruleset: HashMap<String, String>) -> PyResult<Tree>{
    
    let mut tree = Tree::new(tokens);
    let mut new_chunk = true;
    let mut buffer = Vec::<Node>::new();
    let mut new_data = String::from("");

    // Tant que des règles s'appliquent :
    while new_chunk {

        new_chunk = false;

        // On crée le nouveau niveau
        tree.new_level();

        // Pour chaque noeud du niveau précédent :
        for node in tree.previous_level(){

            // Si le contenu du noeud est dans la base de règle, 
            if ruleset.contains_key(&node.data){

                println!("{} : '{:?}'", new_data, buffer);

                // On ajoute le précédent chunk à l'arbre
                tree.add_node(new_data.clone(), buffer.clone());

                // On récupère la donnée du nouveau chunk
                new_data = ruleset.get(&node.data).unwrap().clone();

                // On vide le buffer
                buffer.clear();

                new_chunk = true;

            }

            // On ajoute le noeud au buffer
            buffer.push(node.clone());
        }

        if buffer.len() > 0{
            // S'il reste des tokens dans le buffer, on les ajoute en tant que chunk :

            tree.add_node(new_data.clone(), buffer.clone());

            // On vide le buffer
            buffer.clear();
        }

    }

    //tree.check_integrity();

    return Ok(tree);
}
*/

/* 
/// Moteur à base de règles simple. Il applique les règles données en entrée sur une liste de tokens (chaînes de caractères).
/// 
/// # Paramètres :
/// * `tokens` - la liste des tokens (liste python de chaînes de caractères)
/// * `ruleset` - dictionnaire de règles (dictionnaire python associant une chaîne à une autre chaîne)
#[pyfunction]
fn mbr_deprec(tokens: Vec<String>, ruleset: HashMap<String, String>) -> PyResult<Vec<Vec<(String, Vec<String>)>>>{
    let mut out = Vec::<Vec<(String, Vec<String>)>>::new();

    // First loop on tokens without a type :

    // Setting up buffers
    let mut groups = Vec::<(String, Vec<String>)>::new();
    let mut buffer = Vec::<String>::new();
    let mut chunk_type = String::new();
    let mut new_chunk = true;

    for tok in tokens.iter(){

        if ruleset.contains_key(tok){
            // On commence par enregistrer le chunk précédent :
            groups.push((chunk_type.clone(), buffer.clone()));
            buffer.clear();

            // On peut maintenant setup le nouveau chunk :
            chunk_type = ruleset.get(tok).unwrap().to_string();
            new_chunk = true;
        }

        buffer.push(tok.to_string());
    }

    out.push(groups.clone());
    buffer.clear();
    chunk_type.clear();
    groups.clear();

    while new_chunk{
        new_chunk = false;

        for group in out.last().unwrap(){

            if ruleset.contains_key(&group.0){
                // On commence par enregistrer le chunk précédent :
                groups.push((chunk_type.clone(), buffer.clone()));
                buffer.clear();
    
                // On peut maintenant setup le nouveau chunk :
                chunk_type = ruleset.get(&group.0).unwrap().to_string();
                new_chunk = true;
            }
    
            buffer.append(&mut group.1.clone());
        }

        out.push(groups.clone());
    }

    return Ok(out);
}
*/

/// A Python module implemented in Rust.
#[pymodule]
fn rubelp(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(tokenize, m)?)?;
    m.add_function(wrap_pyfunction!(engine, m)?)?;
    m.add_class::<Node>()?;
    m.add_class::<Tree>()?;
    Ok(())
}