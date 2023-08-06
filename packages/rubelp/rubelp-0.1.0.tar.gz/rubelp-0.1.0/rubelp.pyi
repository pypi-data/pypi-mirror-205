


class Node(object):
    """Classe représentant le noeud d'un arbre, avec pour valeur une chaîne de caractères.

        :param txt: la valeur du noeud
        :type txt: str
        :param lvl: le niveau de l'arbre (coordonnée x)
        :type lvl: int
        :param i: la position du noeud (coordonnée y)
        :type i: int
    """

    def __init__(self, txt: str, lvl: int, i: int):
        ...

    
    def add_child(self, child: Node) -> None:
        """Permet d'ajouter un noeud comme enfant.

        :param child: le nouveau noeud enfant
        :type child: Node
        """


class Tree(object):
    """Classe représentant une arborescence, les noeuds ayant pour seule valeur une chaîne de caractère. 
    Le package utilise cette dernière pour garder une trace de chaque étape de transformation.

    :param leaves: les feuilles de l'arbre
    :type leaves: list[str]
    """

    def __init__(self, leaves: list[str]):
        ...

    def decapsulate(self, lvl: int, i: int) -> list[Node]:
        """Méthode permettant de récupérer les feuilles auquel a accès le noeud spécifié (sous la forme d'une liste de noeuds).

        :param lvl: le niveau de l'arbre (coordonnée x)
        :type lvl: int
        :param i: index du noeud dans le niveau
        :type i: int
        :return: la liste des feuilles
        :rtype: list[Node]
        """

    def concat(self, lvl: int, i: int, sep: str) -> str:
        """Méthode permettant de récupérer le texte des feuilles auquel le noeud a accès, avec possibilité d'un séparateur entre chaque.

        :param lvl: le niveau de l'arbre (coordonnée x)
        :type lvl: int
        :param i: la position du noeud (coordonnée y)
        :type i: int
        :param sep: le séparateur à utiliser
        :type sep: str
        :return: la chaîne résultante
        :rtype: str
        """

    def get_children(self, lvl: int, i: int) -> list[Node]:
        """Méthode permettant de récupérer les enfants du noeud.

        :param lvl: le niveau de l'arbre (coordonnée x)
        :type lvl: int
        :param i: la position du noeud (coordonnée y)
        :type i: int
        :return: la liste des noeuds enfants
        :rtype: list[Node]
        """

    def subtree(self, lvl: int, i: int) -> Tree:
        """Permet de récupérer un sous-arbre sous la forme d'un objet Tree.

        :param lvl: le niveau de l'arbre (coordonnée x)
        :type lvl: int
        :param i: la position du nouveau noeud racine (coordonnée y)
        :type i: int
        :return: le sous arbre partant du noeud spécifié
        :rtype: Tree
        """

    def to_xml(self) -> str:
        """Méthode fournissant une chaîne de caractère décrivant l'arbre au format XML. Format d'export à privilégier.

        :return: l'arbre structuré en XML
        :rtype: str
        """


def engine(tokens: list[str], ruleset: dict) -> Tree:
    """Fonction faisant tourner le moteur à base de règles, à partir de tokens et d'un ensemble de règles.

    :param tokens: la liste des tokens à traiter
    :type tokens: list[str]
    :param ruleset: la base de règles
    :type ruleset: dict
    :return: l'arbre résultant
    :rtype: Tree
    """