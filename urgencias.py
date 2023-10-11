from collections import deque
from tabulate import tabulate

class Paciente:
    def __init__(self, nombre, apellido, edad, identificacion, estado):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.identificacion = identificacion
        self.estado = estado
        self.siguiente = None


class Pila:
    def __init__(self):
        self.item = []
        
    def push(self, items):
        self.item.append(items)
        
    def pop(self):
        if not self.vacia():
            return self.item.pop()
        
    def vacia(self):
        return len(self.item) == 0

class UrgenciasClinica:
    def __init__(self):
        self.pacientes = [] # Arreglo para guardar los pacientes
        self.pacientesAtendidos = [] # Lista simple
        self.pacientesEnEspera = deque() # Cola para los paciente que están en espera
        self.pacientesEnProceso = Pila() # Pila para los pacientes que están en proceso
    
    # Método para registrar los pacientes
    def registrar_pacientes(self, nombre, apellido, edad, identificacion):
        estado = "En espera"
        
        # Verificamos si el paciente está registrado
        for paciente in self.pacientes:
            if paciente.identificacion == identificacion:
                print("\nEste paciente ya está registrado en la sala de urgencias.")
                return
        
        # Si no está registrado, creamos una variable de tipo Paciente y pasamos los datos del paciente   
        nuevoPaciente = Paciente(nombre, apellido, edad, identificacion, estado)
        self.pacientes.append(nuevoPaciente)
        self.pacientesEnEspera.append(nuevoPaciente)
        print("\nPaciente registrado exitosamente.")
    
    # Método para actualizar los datos de un paciente
    def actualizar_pacientes(self, identificacion, nuevoNombre=None, nuevoApellido=None, nuevaEdad=None):
        encontrado = False
        for paciente in self.pacientes:
            # Verificamos si el paciente está registrado
            if paciente.identificacion == identificacion:
                if paciente.estado == "Atendido":
                    print("\nNo se puede cambiar los datos de un cliente atendido.")
                    return
                
                # Pedimos los datos a actualizar
                print(f"\nActualizando datos del paciente con identificación {identificacion} ")
                print("Si no desea actualizar un campo, dejar en blanco")
                nuevoNombre = input("Nuevo nombre: ")
                nuevoApellido = input("Nuevo Apellido: ")
                nuevaEdad = input("Nueva edad: ")
                
                if nuevoNombre != "":
                    paciente.nombre = nuevoNombre
                if nuevoApellido != "":
                    paciente.apellido = nuevoApellido
                if nuevaEdad != "":
                    paciente.edad = nuevaEdad
                
                print("\nDatos del paciente actualizados con éxito.")
                encontrado = True
                break
        if not encontrado:
            print("\nPaciente no encontrado en urgencias.")
    
    # Función para mostrar los pacientes atendidos
    def pacientes_atendidos(self):
        # Verificamos si hay pacientes atendidos
        if not self.pacientesAtendidos:
            print("\nNo hay pacientes atendidos.")
        else:
            headers = ["Nombre", "Apellido", "Edad", "Identificación", "Estado"]
            data = [[paciente.nombre, paciente.apellido, paciente.edad, paciente.identificacion, paciente.estado] for paciente in self.pacientesAtendidos]
            tabla = tabulate(data, headers, tablefmt="grid", numalign="center", stralign="center")
            print("\n-- Pacientes atendidos --")
            print(tabla)
            
            
    # Método para cambiar el estado de un paciente
    def cambiar_estado_pacientes(self, identificacion):
        existePaciente = None
        
        for paciente in self.pacientes:
            # Verificamos si el paciente está registrado
            if paciente.identificacion == identificacion:
                existePaciente = paciente
                break
        
        # Si está registrado mostramos un menú para cambiar el estado
        if existePaciente:
            while True:
                print("""\n
                         -- Estado --
                      1. En espera
                      2. En proceso de atención
                      3. Atendido
                      4. Salir
                      """)
                opcion = int(input("Digite una opción: "))
                
                if opcion == 1:
                    nuevoEstado = "En espera"
                elif opcion == 2:
                    nuevoEstado = "En proceso de atención"
                elif opcion == 3:
                    nuevoEstado = "Atendido"
                elif opcion == 4:
                    break
                else:
                    print("\nOpción no válida.")
                
                if existePaciente.estado == "Atendido":
                    print("\nNo se puede cambiar el estado de un paciente atendido.")
                else:
                    existePaciente.estado = nuevoEstado
                    
                    # Agregamos al paciente a la lista en proceso de atención
                    if nuevoEstado == "En proceso de atención":
                        self.pacientesEnEspera.popleft()
                        self.pacientesEnProceso.push(existePaciente)
                    elif nuevoEstado == "Atendido":
                        self.pacientesEnProceso.pop()
                        self.pacientesAtendidos.append(existePaciente)
                        
                    print("\nEl estado del paciente ha sido actualizado.")
        else:
            print("\nPaciente no encontrado en urgencias.")