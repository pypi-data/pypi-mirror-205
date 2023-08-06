use pyo3::prelude::*;
use crate::node::Node;
use simple_xml_serialize::XMLElement;


/// Tree(leaves: list[str])
/// --
///
/// Classe représentant une arborescence, les noeuds ayant pour seule valeur une chaîne de caractère. 
/// Le package utilise cette dernière pour garder une trace de chaque étape de transformation.
/// 
/// :param leaves: les feuilles de l'arbre
/// :type leaves: list[str]
#[pyclass(module = "rubelp", subclass, text_signature="(leaves: list[str])")]
#[derive(Debug)]
pub struct Tree{
    #[pyo3(get)]
    pub data: Vec<Vec<Node>>
}

#[pymethods]
impl Tree{

    #[new]
    pub fn new(leaves: Vec<String>) -> Self{

        let mut nodes = Vec::<Vec<Node>>::new();
        nodes.push(Vec::<Node>::new());

        /* On ajoute les feuilles de l'arbre, qui constituent le premier niveau. */
        for (i, leaf) in leaves.iter().enumerate(){
            nodes[0].push(Node::new(leaf.clone(), i, 0));
        }

        Tree { data: nodes }
    }

    /// decapsulate(self, lvl: int, i: int)
    ///
    /// Méthode permettant de récupérer les feuilles auquel a accès le noeud spécifié (sous la forme d'une liste de noeuds).
    /// :param lvl: le niveau de l'arbre (coordonnée x)
    /// :type lvl: int
    /// :param i: index du noeud dans le niveau
    /// :type i: int
    /// :return: la liste des feuilles
    /// :rtype: list[Node]
    pub fn decapsulate(&self, lvl: usize, i: usize) -> PyResult<Vec<Node>>{

        let mut out = Vec::<Node>::new();

        if lvl == 0{
            return Ok(out);
        }

        for child in self.data[lvl][i].children.iter(){

            let node = self.data[lvl-1][child.clone()].clone();

            if node.level == 0{
                out.push(node);
            }
            else{
                out.append(&mut self.decapsulate(node.level, node.index).unwrap());
            }
        }

        Ok(out)
    }

    /// concat(self, lvl: int, i: int, sep: str)
    /// 
    /// Méthode permettant de récupérer le texte des feuilles auquel le noeud a accès, avec possibilité d'un séparateur entre chaque.
    /// 
    /// :param lvl: le niveau de l'arbre (coordonnée x)
    /// :type lvl: int
    /// :param i: la position du noeud (coordonnée y)
    /// :type i: int
    /// :param sep: le séparateur à utiliser
    /// :type sep: str
    /// :return: la chaîne résultante
    /// :rtype: str
    pub fn concat(&self, lvl: usize, i: usize, sep: &str) -> PyResult<String>{

        let nodes = self.decapsulate(lvl, i).unwrap();

        let strs: Vec<String> = nodes.into_iter().map(|x| x.data).collect();

        Ok(strs.join(sep))
    }

    /// get_children(self, lvl: int, i: int)
    /// 
    /// Méthode permettant de récupérer les enfants du noeud.
    ///
    /// :param lvl: le niveau de l'arbre (coordonnée x)
    /// :type lvl: int
    /// :param i: la position du noeud (coordonnée y)
    /// :type i: int
    /// :return: la liste des noeuds enfants
    /// :rtype: list[Node]
    pub fn get_children(&self, lvl: usize, i: usize) -> PyResult<Vec<Node>>{

        let root = self.data[lvl][i].clone();
        let children_coords = root.children;

        let mut children = Vec::<Node>::new();

        for child in children_coords{
            children.push(self.data[lvl-1][child].clone());
        }

        Ok(children)
    }

    /// subtree(self, lvl: int, i: int)
    /// 
    /// Permet de récupérer un sous-arbre sous la forme d'un objet Tree.
    /// :param lvl: le niveau de l'arbre (coordonnée x)
    /// :type lvl: int
    /// :param i: la position du nouveau noeud racine (coordonnée y)
    /// :type i: int
    /// :return: le sous arbre partant du noeud spécifié
    /// :rtype: Tree
    pub fn subtree(&self, lvl: usize, i: usize) -> PyResult<Tree>{

        //FIXME: données qui disparaissent + modifier les coordonnées de chaque noeud pour s'accorder avec le nouvel arbre

        // Cette méthode implémente un parcours d'arbre en longueur ; voir la sérialisation XML pour un exemple de parcours en profondeur

        // On récupère le noeud racine et on crée la structure de base de l'arbre
        let root = self.data[lvl][i].clone();
        let mut nodes = Vec::<Vec<Node>>::new();

        // On initialise les variables de bouclage (qui vont évoluer à chaque itération)
        let mut probe = lvl;
        let mut current_nodes = vec![root];
        

        while probe > 0{

            let mut next_line = Vec::<Node>::new();

            nodes.push(current_nodes.clone()); // On ajoute la ligne courante à l'arbre

            // Pour chaque noeud de la ligne courante, on récupère leurs enfants et on génère ainsi la ligne inférieure
            for node in current_nodes{
                let mut children = self.get_children(probe, node.index).unwrap();
                next_line.append(&mut children);
            }

            current_nodes = next_line.clone();
            probe -= 1;

        }

        nodes.reverse();

        Ok(Tree{data: nodes})
    }

    /// to_xml(self)
    /// 
    /// Méthode fournissant une chaîne de caractère décrivant l'arbre au format XML. Format d'export à privilégier.
    /// 
    /// :return: l'arbre structuré en XML
    /// :rtype: str
    pub fn to_xml(&self) -> PyResult<String>{
        let mut root = XMLElement::new("test");

        for node in self.data[if self.data.len() > 0 {self.data.len()-1} else {0}].iter(){
            root.add_element(self.node_to_xml(node.level, node.index))
        }

        Ok(root.to_string_pretty("\n", "\t"))
    }


}


impl Tree{


    pub fn add_node(& mut self, txt:String, children: Vec<Node>) -> Node{
        
        // On crée le nouveau noeud en calculant ses indices

        let level_size = self.data.len()-1;

        let i = if self.data[level_size].len() > 0 { self.data[level_size].len()-1 } else { 0 };
        let lvl = level_size;

        let mut new_node = Node::new(txt.clone(), lvl, i);

        // On récupère l'index de chaque enfant du nouveau noeud
        for child in children{
            new_node.children.push(child.index);
        }

        // On ajoute le nouveau noeud à l'arbre
        self.data[level_size].push(new_node.clone());

        new_node
    }

    pub fn last_level(&self) -> Vec<Node>{

        self.data.last().cloned().unwrap()
    }

    pub fn previous_level(&self) -> Vec<Node>{

        // Si l'on a au moins deux niveaux, on peut retourner l'avant-dernier, sinon on retourne le dernier.
        if self.data.len() >1{
            return self.data[self.data.len()-2].clone();
        }
        else{
            return self.data[self.data.len()-1].clone();
        }
        
    }

    pub fn new_level(&mut self){
        self.data.push(Vec::<Node>::new());
    }

    fn node_to_xml(&self, lvl: usize, i: usize) -> XMLElement{
        println!("lvl : {} ; i : {}", lvl, i);
        let node = &self.data[lvl][i];

        let mut el = XMLElement::new("chunk");

        if lvl != 0{
            el.add_attr("type", node.data.clone());
        }
        else{
            el.set_text(node.data.clone());
        }

        for child in node.children.iter(){
            el.add_element(self.node_to_xml(lvl-1, child.clone()));
        }

        el
        
    }


    pub fn check_integrity(&mut self){


        if self.data[self.data.len()-1].len() == 0{
            self.data.remove(self.data.len()-1);
        }

        /*let mut offset = 0;
        
        for (i, level) in self.data.to_owned().iter().enumerate(){
            if level.len() == 0{
                self.data.remove(i);
                offset += 1;
                continue;
            }

            if offset > 0{
                let row = self.data[i].clone();
                let mut new_row = Vec::<Node>::new();

                for node in row.iter(){
                    let mut new_node = node.clone();
                    new_node.level -= offset;
                    new_row.push(new_node);
                }

                self.data[i] = new_row;
            }

        }*/
    }

}


impl From<Vec<Node>> for Tree{
    
    fn from(nodes : Vec<Node>) -> Self{

        let mut ns = Vec::<Vec<Node>>::new();
        ns.push(nodes);

        Tree { data: ns }
    }
}

impl From<Vec<Vec<Node>>> for Tree{

    fn from(nodes : Vec<Vec<Node>>) -> Self{

        Tree { data: nodes }
    }
}

