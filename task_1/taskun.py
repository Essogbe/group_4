from typing import Union, List,Tuple
class Array:
    def __init__(self, data: Union[List[Union[float, int]], List[List[Union[float, int]]]]):
        
        #s.assurer qu'on a une liste en entrée'
        if not isinstance(data, list):
            raise TypeError("data must be a list of integers or a list of lists of integers or floaters.")
            
        #s'assurer qu'on a un tableau d'entiers ou un tableau de tableau d'entiers'      
        if not(
          all(isinstance(i, Union[float, int]) for i in data) or          all(isinstance(i, list) and all(isinstance(j, Union[float, int]) for j in i) for i in data)):
            raise TypeError("data must be a list of integers or a list of lists of integers or floaters.")
        
        self.data =data.copy()

        #cas de 2d ( chaque liste dans la liste est aussi un Array)
        if all(isinstance(i, Union[float, int]) for i in data):
            self.shape = (len(data),)
        else:
            self.shape = (len(data), len(data[0]))
        
        
      
        
              
        # Pour obtenir un élément spécifique ou une tranche du tableau
    def __getitem__(self, index: Union[int, Tuple[Union[float, int], Union[float, int]]]) -> Union[Union[float, int], List[Union[float, int]]]:
        
        if isinstance(index, tuple):
            return self.data[index[0]][index[1]]  # Tableau 2D
        else:
            return self.data[index]  # Tableau 1D      


    #len
    def __len__(self) -> int:
        return len(self.data) if self.shape == (len(self.data),) else self.shape[0]
        
    #Fonction de division    
    def __truediv__(self, other: Union['Array', int, float]) -> 'Array': 
        """
        Surcharge l'opérateur de division pour la classe Array.

        other: Peut être une autre instance de la classe Array ou un entier (int) ou un flottant (float).
        retourne une nouvelle instance de la classe Array résultant de la division.
        """

        if isinstance(other, Union[float, int]): #Dans  ce cas, other est un entier ou un flottant
            return Array([[item / other for item in row] for row in self.data])
        elif self.shape != other.shape: # Vérifie si les dimensions de self et de other correspondent
            raise ValueError("Shapes do not match for division") #Lève une exception si ce n'est pas le cas
        else: #Dans ce cas, other est un array
            return Array([[self.data[i][j] / other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
        
    #Fonction de multiplication
    def __mul__(self, other: Union['Array', int, float]) -> 'Array':
        """
        Surcharge l'opérateur de multiplication pour la classe Array.
        other: Peut être une autre instance de la classe Array ou un entier (int) ou un flottant (float).
        retourne une nouvelle instance de la classe Array résultant de la division.
        """
        if isinstance(other, Union[float, int]): #Dans  ce cas, other est un entier ou un flottant
            return Array([[item * other for item in row] for row in self.data])
        elif self.shape != other.shape: # Vérifie si les dimensions de self et de other correspondent
            raise ValueError("Shapes do not match for multiplication") #Lève une exception si ce n'est pas le cas
        else: #Dans ce cas, other est un array
            return Array([[self.data[i][j] * other.data[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
        


        
    def __repr__(self):
            return f"Array({self.data})"
    
#test
if __name__ == "__main__":
    tableau11=Array([[4,6,2],[8,2,5]])
    tableau2=Array([[3,4,6],[3,1,2]])
    print(tableau11)
    print(tableau2)
    print(tableau11 / tableau2)
    print(tableau11 * tableau2)
    print(tableau11 / 8)