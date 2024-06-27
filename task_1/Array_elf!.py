from typing import Union, List,Tuple , Any
class Array:
    def __init__(self, data: Union[List[int], List[List[int]]]):
        
        #s.assurer qu'on a une liste en entrée'
        if not isinstance(data, (list, )):
            raise TypeError("data must be a list of integers or a list of lists of integers.")
            
        #s'assurer qu'on a un tableau d'entiers ou un tableau de tableau d'entiers'      
        if not(all(isinstance(i, int) for i in data) or all(isinstance(i, list) and all(isinstance(j, int) for j in i) for i in data)):
            raise TypeError("data must be a list of integers or a list of lists of integers.")
        
        self.data =data.copy()
        #cas de 2d ( chaque liste dans la liste est aussi un Array)
        if isinstance(data[0],list):
            for i in range(self.data):
                self.data[i] =Array(self.data[i])
        # Initialise la forme de nos tableau
        if isinstance(data[0], list):
            self.shape = (len(data), len(data[0]))
        else:
            self.shape = (len(data),)
        
    def __len__(self) -> int:
        return len(self.data) if self.shape == (len(self.data),) else self.shape[0]
              
        # Pour obtenir un élément spécifique ou une tranche du tableau
    def __getitem__(self, index: Union[int, Tuple[int, int]]) -> Union[int, List[int]]:
        
        if isinstance(index, tuple):
            return self.data[index[0]][index[1]]  # Tableau 2D
        else:
            return self.data[index]  # Tableau 1D      
    # Le produit scalaire avec deux Tableau 1d et de même taille 

    def __matmul__(self , other:'Array')->Union[int , float]:
        if self.shape != other.shape or len(self.data)!= len(other.data): 
            raise ValueError ('Cette opération est uniquement sur les array 1d et qui sont de même taille')
        return sum(element_self * element_other for element_self, element_other in zip(self.data, other.data))
    # Fonction pour la Recherche avec l'opérateur 'in'
    def __contains__(self, item: Any) -> bool:
        if len(self.shape) == 1:
            return item in self.data
        else:
            return any(item in row for row in self.data)
        
if __name__== "__main__":
    # initialisez nos deux tableau pour le test  
    tableau_1d_2 = Array([5 , 4, 3, 2, 1])
    tableau_1d = Array([1, 2, 3, 4, 5])
    #Visualiser la taille et la forme de chacun de not tableau
    print(len(tableau_1d))
    print(tableau_1d.shape)

    print(len(tableau_1d_2))
    print(tableau_1d_2.shape)

    #fire la recherche
    print(3 in tableau_1d) 

    #Produit scalaire
    Res = tableau_1d @ tableau_1d_2
    print(Res)