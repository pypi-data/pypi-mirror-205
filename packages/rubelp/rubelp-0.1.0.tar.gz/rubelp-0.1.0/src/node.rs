use pyo3::prelude::*;


/// Node(txt: str, lvl: int, i: int)
/// --
///
/// Classe représentant le noeud d'un arbre, avec pour valeur une chaîne de caractères.
/// 
/// :param txt: la valeur du noeud
/// :type txt: str
/// :param lvl: le niveau de l'arbre (coordonnée x)
/// :type lvl: int
/// :param i: la position du noeud (coordonnée y)
/// :type i: int
#[pyclass(module = "rubelp", subclass, text_signature="(txt: str, i: int, lvl: int)")]
#[derive(Clone)]
#[derive(Debug)]
pub struct Node{
    #[pyo3(get)]
    pub children: Vec<usize>,
    #[pyo3(get)]
    pub data: String,
    #[pyo3(get)]
    pub index: usize,
    #[pyo3(get)]
    pub level: usize
}

#[pymethods]
impl Node{

    #[new]
    pub fn new(txt: String, lvl: usize, i: usize) -> Self{
        Node { 
            data: txt, 
            index: i, 
            level: lvl, 
            children: Vec::<usize>::new()
        }
    }

}


impl Node{

    pub fn add_child(&mut self, child: &Node) -> (){

        self.children.push(child.index);

        ()
    }

}
