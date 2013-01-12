from random import randint

class Wolfram():
    '''
    Implementa un automata celular de una dimension, revisando 
    cuatro posibles estados por celda

    :param num_cells: numero de celdas a generar
    :type num_cells: int
    '''
    def __init__(self,num_cells=5):
        self.num_cells = num_cells
        self.rules=[] #reglas
        self.cells=[] #contenido
        self.generation = 0 #numero de generaciones

        for i in range(self.num_cells):
            self.cells.append(randint(0,4))

        for i in range(125):
            self.rules.append(randint(0,4))

    def randomize(self):
        '''
        Regenera las reglas y celdas del sistema
        '''
        for i in range(125):
            self.rules[i] = randint(0,4)
        
        for i in range(self.num_cells):
            self.cells[i] = randint(0,4)
    
    def generate(self):
        '''
        Aplica las reglas de evolucion, revisando el estado de
        la celda y los vecinos cerca. Las celdas de los extremos
        estan definidas para comportarse como un espacio cilindrico

        :returns: lista con la nueva generacion
        '''
        nextgen = [] #donde va a guardar la nueva generacion
        for index,cell in enumerate(self.cells):
            #revisa si es el primer elemento de la lista
            if not index == 0: 
                left = self.cells[index-1]
            else:
                left = self.cells[-1] #toma el ultimo valor de la lista

            me = cell

            #revisa si es el ultimo elemento
            if not index == len(self.cells)-1:
                right = self.cells[index+1]
            else:
                right = self.cells[0] #toma el primer elemento de la lista
            
            #aplica las reglas
            nextgen.append(self.compute_rules(left,me,right)) 
        
        #revisa que el nuevo estado sea diferente al anterior
        #de lo contrario regenera el sistema
        if not self.cells == nextgen:  
            self.cells = nextgen[:]
        else:
            self.randomize()
            self.generate()
            self.generation = 0
        self.generation +=1

        return self.cells 

    def compute_rules(self,lft, me, rght):
        '''
        Reglas del sistema para cada caso posible
        '''
        if lft == 0 and me == 0 and rght == 0: return self.rules[0]
        if lft == 0 and me == 0 and rght == 1: return self.rules[1]
        if lft == 0 and me == 0 and rght == 2: return self.rules[2]
        if lft == 0 and me == 0 and rght == 3: return self.rules[3]
        if lft == 0 and me == 0 and rght == 4: return self.rules[4]
        if lft == 0 and me == 1 and rght == 0: return self.rules[5]
        if lft == 0 and me == 1 and rght == 1: return self.rules[6]
        if lft == 0 and me == 1 and rght == 2: return self.rules[7]
        if lft == 0 and me == 1 and rght == 3: return self.rules[8]
        if lft == 0 and me == 1 and rght == 4: return self.rules[9]
        if lft == 0 and me == 2 and rght == 0: return self.rules[10]
        if lft == 0 and me == 2 and rght == 1: return self.rules[11]
        if lft == 0 and me == 2 and rght == 2: return self.rules[12]
        if lft == 0 and me == 2 and rght == 3: return self.rules[13]
        if lft == 0 and me == 2 and rght == 4: return self.rules[14]
        if lft == 0 and me == 3 and rght == 0: return self.rules[15]
        if lft == 0 and me == 3 and rght == 1: return self.rules[16]
        if lft == 0 and me == 3 and rght == 2: return self.rules[17]
        if lft == 0 and me == 3 and rght == 3: return self.rules[18]
        if lft == 0 and me == 3 and rght == 4: return self.rules[19]
        if lft == 0 and me == 4 and rght == 0: return self.rules[20]
        if lft == 0 and me == 4 and rght == 1: return self.rules[21]
        if lft == 0 and me == 4 and rght == 2: return self.rules[22]
        if lft == 0 and me == 4 and rght == 3: return self.rules[23]
        if lft == 0 and me == 4 and rght == 4: return self.rules[24]
        if lft == 1 and me == 0 and rght == 0: return self.rules[25]
        if lft == 1 and me == 0 and rght == 1: return self.rules[26]
        if lft == 1 and me == 0 and rght == 2: return self.rules[27]
        if lft == 1 and me == 0 and rght == 3: return self.rules[28]
        if lft == 1 and me == 0 and rght == 4: return self.rules[29]
        if lft == 1 and me == 1 and rght == 0: return self.rules[30]
        if lft == 1 and me == 1 and rght == 1: return self.rules[31]
        if lft == 1 and me == 1 and rght == 2: return self.rules[32]
        if lft == 1 and me == 1 and rght == 3: return self.rules[33]
        if lft == 1 and me == 1 and rght == 4: return self.rules[34]
        if lft == 1 and me == 2 and rght == 0: return self.rules[35]
        if lft == 1 and me == 2 and rght == 1: return self.rules[36]
        if lft == 1 and me == 2 and rght == 2: return self.rules[37]
        if lft == 1 and me == 2 and rght == 3: return self.rules[38]
        if lft == 1 and me == 2 and rght == 4: return self.rules[39]
        if lft == 1 and me == 3 and rght == 0: return self.rules[40]
        if lft == 1 and me == 3 and rght == 1: return self.rules[41]
        if lft == 1 and me == 3 and rght == 2: return self.rules[42]
        if lft == 1 and me == 3 and rght == 3: return self.rules[43]
        if lft == 1 and me == 3 and rght == 4: return self.rules[44]
        if lft == 1 and me == 4 and rght == 0: return self.rules[45]
        if lft == 1 and me == 4 and rght == 1: return self.rules[46]
        if lft == 1 and me == 4 and rght == 2: return self.rules[47]
        if lft == 1 and me == 4 and rght == 3: return self.rules[48]
        if lft == 1 and me == 4 and rght == 4: return self.rules[49]
        if lft == 2 and me == 0 and rght == 0: return self.rules[50]
        if lft == 2 and me == 0 and rght == 1: return self.rules[51]
        if lft == 2 and me == 0 and rght == 2: return self.rules[52]
        if lft == 2 and me == 0 and rght == 3: return self.rules[53]
        if lft == 2 and me == 0 and rght == 4: return self.rules[54]
        if lft == 2 and me == 1 and rght == 0: return self.rules[55]
        if lft == 2 and me == 1 and rght == 1: return self.rules[56]
        if lft == 2 and me == 1 and rght == 2: return self.rules[57]
        if lft == 2 and me == 1 and rght == 3: return self.rules[58]
        if lft == 2 and me == 1 and rght == 4: return self.rules[59]
        if lft == 2 and me == 2 and rght == 0: return self.rules[60]
        if lft == 2 and me == 2 and rght == 1: return self.rules[61]
        if lft == 2 and me == 2 and rght == 2: return self.rules[62]
        if lft == 2 and me == 2 and rght == 3: return self.rules[63]
        if lft == 2 and me == 2 and rght == 4: return self.rules[64]
        if lft == 2 and me == 3 and rght == 0: return self.rules[65]
        if lft == 2 and me == 3 and rght == 1: return self.rules[66]
        if lft == 2 and me == 3 and rght == 2: return self.rules[67]
        if lft == 2 and me == 3 and rght == 3: return self.rules[68]
        if lft == 2 and me == 3 and rght == 4: return self.rules[69]
        if lft == 2 and me == 4 and rght == 0: return self.rules[70]
        if lft == 2 and me == 4 and rght == 1: return self.rules[71]
        if lft == 2 and me == 4 and rght == 2: return self.rules[72]
        if lft == 2 and me == 4 and rght == 3: return self.rules[73]
        if lft == 2 and me == 4 and rght == 4: return self.rules[74]
        if lft == 3 and me == 0 and rght == 0: return self.rules[75]
        if lft == 3 and me == 0 and rght == 1: return self.rules[76]
        if lft == 3 and me == 0 and rght == 2: return self.rules[77]
        if lft == 3 and me == 0 and rght == 3: return self.rules[78]
        if lft == 3 and me == 0 and rght == 4: return self.rules[79]
        if lft == 3 and me == 1 and rght == 0: return self.rules[80]
        if lft == 3 and me == 1 and rght == 1: return self.rules[81]
        if lft == 3 and me == 1 and rght == 2: return self.rules[82]
        if lft == 3 and me == 1 and rght == 3: return self.rules[83]
        if lft == 3 and me == 1 and rght == 4: return self.rules[84]
        if lft == 3 and me == 2 and rght == 0: return self.rules[85]
        if lft == 3 and me == 2 and rght == 1: return self.rules[86]
        if lft == 3 and me == 2 and rght == 2: return self.rules[87]
        if lft == 3 and me == 2 and rght == 3: return self.rules[88]
        if lft == 3 and me == 2 and rght == 4: return self.rules[89]
        if lft == 3 and me == 3 and rght == 0: return self.rules[90]
        if lft == 3 and me == 3 and rght == 1: return self.rules[91]
        if lft == 3 and me == 3 and rght == 2: return self.rules[92]
        if lft == 3 and me == 3 and rght == 3: return self.rules[93]
        if lft == 3 and me == 3 and rght == 4: return self.rules[94]
        if lft == 3 and me == 4 and rght == 0: return self.rules[95]
        if lft == 3 and me == 4 and rght == 1: return self.rules[96]
        if lft == 3 and me == 4 and rght == 2: return self.rules[97]
        if lft == 3 and me == 4 and rght == 3: return self.rules[98]
        if lft == 3 and me == 4 and rght == 4: return self.rules[99]
        if lft == 4 and me == 0 and rght == 0: return self.rules[100]
        if lft == 4 and me == 0 and rght == 1: return self.rules[101]
        if lft == 4 and me == 0 and rght == 2: return self.rules[102]
        if lft == 4 and me == 0 and rght == 3: return self.rules[103]
        if lft == 4 and me == 0 and rght == 4: return self.rules[104]
        if lft == 4 and me == 1 and rght == 0: return self.rules[105]
        if lft == 4 and me == 1 and rght == 1: return self.rules[106]
        if lft == 4 and me == 1 and rght == 2: return self.rules[107]
        if lft == 4 and me == 1 and rght == 3: return self.rules[108]
        if lft == 4 and me == 1 and rght == 4: return self.rules[109]
        if lft == 4 and me == 2 and rght == 0: return self.rules[110]
        if lft == 4 and me == 2 and rght == 1: return self.rules[111]
        if lft == 4 and me == 2 and rght == 2: return self.rules[112]
        if lft == 4 and me == 2 and rght == 3: return self.rules[113]
        if lft == 4 and me == 2 and rght == 4: return self.rules[114]
        if lft == 4 and me == 3 and rght == 0: return self.rules[115]
        if lft == 4 and me == 3 and rght == 1: return self.rules[116]
        if lft == 4 and me == 3 and rght == 2: return self.rules[117]
        if lft == 4 and me == 3 and rght == 3: return self.rules[118]
        if lft == 4 and me == 3 and rght == 4: return self.rules[119]
        if lft == 4 and me == 4 and rght == 0: return self.rules[120]
        if lft == 4 and me == 4 and rght == 1: return self.rules[121]
        if lft == 4 and me == 4 and rght == 2: return self.rules[122]
        if lft == 4 and me == 4 and rght == 3: return self.rules[123]
        if lft == 4 and me == 4 and rght == 4: return self.rules[124]


