from typing import Union, List, Tuple


class Array:
    def __init__(self, data: Union[List[int], List[List[int]], List['Array']]):
        # Vérifie que data est une liste
        if not isinstance(data, list):
            raise TypeError("data must be a list of integers or a list of lists of integers.")

        # Vérifie que data est une liste d'entiers, une liste de listes d'entiers, ou une liste d'objets Array
        if not (
                all(isinstance(i, int) for i in data) or
                all(isinstance(i, list) and all(isinstance(j, int) for j in i) for i in data) or
                all(isinstance(i, Array) for i in data)):
            raise TypeError("data must be a list of integers, a list of lists of integers, or a list of Array objects.")

        # Copie des données pour éviter les modifications externes
        self.data = data.copy()

        # Si data est une liste de listes, transforme chaque sous-liste en objet Array
        if isinstance(data[0], list):
            for i in range(len(self.data)):
                self.data[i] = Array(self.data[i])

    def __getitem__(self, index: Union[int, Tuple[int, int]]) -> Union[int, List[int]]:
        # Accès aux éléments spécifiques avec un index unique ou un couple d'indices
        if isinstance(index, tuple):
            return self.data[index[0]][index[1]]
        else:
            return self.data[index]

    def __setitem__(self, index: Union[int, Tuple[int, int]], value: int):
        # Modification des éléments avec un index unique ou un couple d'indices
        if isinstance(index, tuple):
            self.data[index[0]][index[1]] = value
        else:
            self.data[index] = value

    def __add__(self, other: 'Array') -> 'Array':
        # Vérifie que other est un objet Array
        if isinstance(other, Array):
            # Addition élément par élément pour les tableaux 2D
            if isinstance(self.data[0], Array):
                return Array([self.data[i] + other.data[i] for i in range(len(self.data))])
            # Addition élément par élément pour les tableaux 1D
            elif isinstance(self.data[0], list):
                return Array([[self.data[i][j] + other.data[i][j] for j in range(len(self.data[i]))] for i in
                              range(len(self.data))])
            else:
                return Array([self.data[i] + other.data[i] for i in range(len(self.data))])
        else:
            raise TypeError("Both operands must be of type 'Array'")

    def __sub__(self, other: 'Array') -> 'Array':
        # Vérifie que other est un objet Array
        if isinstance(other, Array):
            # Soustraction élément par élément pour les tableaux 2D
            if isinstance(self.data[0], Array):
                return Array([self.data[i] - other.data[i] for i in range(len(self.data))])
            # Soustraction élément par élément pour les tableaux 1D
            elif isinstance(self.data[0], list):
                return Array([[self.data[i][j] - other.data[i][j] for j in range(len(self.data[i]))] for i in
                              range(len(self.data))])
            else:
                return Array([self.data[i] - other.data[i] for i in range(len(self.data))])
        else:
            raise TypeError("Both operands must be of type 'Array'")

    def __mul__(self, other: Union[int, 'Array']) -> 'Array':
        # Vérifie que other est un objet Array ou un entier
        if isinstance(other, Array):
            # Multiplication élément par élément pour les tableaux 2D
            if isinstance(self.data[0], Array):
                return Array([self.data[i] * other.data[i] for i in range(len(self.data))])
            # Multiplication élément par élément pour les tableaux 1D
            elif isinstance(self.data[0], list):
                return Array([[self.data[i][j] * other.data[i][j] for j in range(len(self.data[i]))] for i in
                              range(len(self.data))])
            else:
                return Array([self.data[i] * other.data[i] for i in range(len(self.data))])
        elif isinstance(other, int):
            # Multiplication par un scalaire pour les tableaux 2D
            if isinstance(self.data[0], Array):
                return Array([self.data[i] * other for i in range(len(self.data))])
            # Multiplication par un scalaire pour les tableaux 1D
            elif isinstance(self.data[0], list):
                return Array(
                    [[self.data[i][j] * other for j in range(len(self.data[i]))] for i in range(len(self.data))])
            else:
                return Array([self.data[i] * other for i in range(len(self.data))])
        else:
            raise TypeError("Operand must be of type 'int' or 'Array'")

    def __truediv__(self, other: Union[int, 'Array']) -> 'Array':
        # Vérifie que other est un objet Array ou un entier
        if isinstance(other, Array):
            # Division élément par élément pour les tableaux 2D
            if isinstance(self.data[0], Array):
                return Array([self.data[i] / other.data[i] for i in range(len(self.data))])
            # Division élément par élément pour les tableaux 1D
            elif isinstance(self.data[0], list):
                return Array([[self.data[i][j] / other.data[i][j] for j in range(len(self.data[i]))] for i in
                              range(len(self.data))])
            else:
                return Array([self.data[i] / other.data[i] for i in range(len(self.data))])
        elif isinstance(other, int):
            # Division par un scalaire pour les tableaux 2D
            if isinstance(self.data[0], Array):
                return Array([self.data[i] / other for i in range(len(self.data))])
            # Division par un scalaire pour les tableaux 1D
            elif isinstance(self.data[0], list):
                return Array(
                    [[self.data[i][j] / other for j in range(len(self.data[i]))] for i in range(len(self.data))])
            else:
                return Array([self.data[i] / other for i in range(len(self.data))])
        else:
            raise TypeError("Operand must be of type 'int' or 'Array'")

    def __matmul__(self, other: 'Array') -> int:
        # Vérifie que les deux tableaux sont 1D
        if isinstance(self.data[0], list) or isinstance(other.data[0], list):
            raise ValueError("Matrix multiplication is only supported for 1D arrays")
        else:
            # Produit scalaire des deux tableaux 1D
            return sum(self.data[i] * other.data[i] for i in range(len(self.data)))

    def __contains__(self, item: int) -> bool:
        # Vérifie la présence d'un élément dans le tableau
        if isinstance(self.data[0], list):
            return any(item in sublist for sublist in self.data)
        else:
            return item in self.data

    def __repr__(self) -> str:
        # Représentation de l'objet Array
        return f"Array(data={self.data})"

    def __len__(self) -> int:
        # Retourne la longueur de l'objet Array (nombre d'éléments dans la liste principale)
        return len(self.data)


# Exemples d'utilisation de la classe Array
if __name__ == "__main__":
    a = Array([1, 2, 3, 4, 5])  # Tableau 1D
    b = Array([5, 4, 3, 2, 1])  # Tableau 1D
    c = a + b  # Addition des tableaux
    d = a * 2  # Multiplication par un scalaire
    e = a @ b  # Produit scalaire

    print(f"a: {a}")
    print(f"b: {b}")
    print(f"c: {c}")
    print(f"d: {d}")
    print(f"e: {e}")
    print(len(a))

    f = Array([[1, 2], [3, 4]])  # Tableau 2D
    g = Array([[4, 3], [2, 1]])  # Tableau 2D
    h = f + g  # Addition des tableaux
    i = f * 2  # Multiplication par un scalaire

    print(f"f: {f}")
    print(f"g: {g}")
    print(f"h: {h}")
    print(f"i: {i}")
