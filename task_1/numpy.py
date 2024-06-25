from typing import Union, List, Tuple


class Array:
    def __init__(self, data: Union[List[int], List[List[int]]]):

        # s.assurer qu'on a une liste en entrée'
        if not isinstance(data, (list,)):
            raise TypeError("data must be a list of integers or a list of lists of integers.")

        # s'assurer qu'on a un tableau d'entiers ou un tableau de tableau d'entiers'
        if not (
                all(isinstance(i, int) for i in data) or all(
            isinstance(i, list) and all(isinstance(j, int) for j in i) for i in data)):
            raise TypeError("data must be a list of integers or a list of lists of integers.")

        self.data = data.copy()
        # cas de 2d ( chaque liste dans la liste est aussi un Array)
        if isinstance(data[0], list):
            for i in range(self.data):
                self.data[i] = Array(self.data[i])

        # Pour obtenir un élément spécifique ou une tranche du tableau

    def __getitem__(self, index: Union[int, Tuple[int, int]]) -> Union[int, List[int]]:

        if isinstance(index, tuple):
            return self.data[index[0]][index[1]]  # Tableau 2D
        else:
            return self.data[index]  # Tableau 1D
