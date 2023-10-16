# Lista doblemente enlazada
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None
        
class ListaDobleEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        
    def estaVacia(self):
        return self.primero is None
        
    def insertarInicio(self, dato):
        nuevoNodo = Nodo(dato)
        
        if self.primero is None:
            self.primero = nuevoNodo
            self.ultimo = nuevoNodo
        else:
            nuevoNodo.siguiente = self.primero
            self.primero.anterior = nuevoNodo
            self.primero = nuevoNodo
            
    def insertarFinal(self, dato):
        nuevoNodo = Nodo(dato)
        
        if self.primero is None:
            self.primero = nuevoNodo
            self.ultimo = nuevoNodo
        else:
            nuevoNodo.anterior = self.ultimo
            self.ultimo.siguiente = nuevoNodo
            self.ultimo = nuevoNodo
            
    def buscar(self, dato):
        nodoActual = self.primero
        
        while nodoActual is not None:
            if nodoActual == dato:
                return nodoActual
            nodoActual = nodoActual.siguiente
        return None
    
    def eliminar(self, dato):
        nodoActual = self.primero
        
        while nodoActual is not None:
            if nodoActual.dato == dato:
                if nodoActual == self.primero:
                    self.primero = self.primero.siguiente
                    if self.primero is not None:
                        self.primero.anterior = None
                else:
                    if nodoActual == self.ultimo:
                        self.ultimo = self.ultimo.anterior
                        self.ultimo.siguiente = None
                    else:
                        nodoActual.anterior.siguiente = nodoActual.siguiente
                        nodoActual.siguiente.anterior =nodoActual.anterior
                return 
            nodoActual = nodoActual.siguiente
            
    def mostrar(self):
        nodoActual = self.primero
        
        while nodoActual is not None:
            print(nodoActual.dato)
            nodoActual = nodoActual.siguiente
            
# Pila
class Pila:
    def __init__(self):
        self.item = []
        
    def agregar(self, items):
        self.item.append(items)
        
    def eliminar(self, items=None):
        if items is not None:
            if items in self.item:
                self.item.remove(items)
                return items
            else:
                return None
        else:
            if not self.vacia():
                return self.item.pop()
        
    def vacia(self):
        return len(self.item) == 0
    
# Cola
class Cola:
    def __init__(self):
        self.item = []
        
    def agregar(self, items):
        self.item.append(items)
        
    def eliminar(self):
        if not self.vacia:
            return self.item.pop(0)
    
    def vacia(self):
        return len(self.item) == 0
    
    def __iter__(self):
        return iter(self.item)