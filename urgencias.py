from estructuras import ListaDobleEnlazada as listaDoble
from estructuras import Pila
from estructuras import Cola

class Paciente:
    def __init__(self, nombre, apellido, edad, identificacion, estado):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.identificacion = identificacion
        self.estado = estado

class ClinicaUrgencias:
    def __init__(self):
        self.pacientes = Cola() # Cola para guardar los pacientes para guardar por orden de llegada
        self.pacientesAtendidos = [] # Lista simple
        self.pacientesEnEspera = listaDoble() # Lista doble para los pacientes en espera
        self.pacientesEnProceso = Pila() # Pila para los pacientes que están en proceso
    
    # Método para registrar los pacientes
    def registrarPaciente(self, nombre, apellido, edad, identificacion):
        estado = "En espera"
        
        # Verificamos si el paciente está registrado
        for paciente in self.pacientes:
            if paciente.identificacion == identificacion:
                print("\nEste paciente ya está registrado en la sala de urgencias.")
                return
        
        # Si no está registrado, creamos una variable de tipo Paciente y pasamos los datos del paciente   
        nuevoPaciente = Paciente(nombre, apellido, edad, identificacion, estado)
        self.pacientes.agregar(nuevoPaciente)
        self.pacientesEnEspera.insertarFinal(nuevoPaciente)
        print("\nPaciente registrado exitosamente.")
    
    # Método para actualizar los datos de un paciente
    def actualizarPaciente(self, identificacion, nuevoNombre=None, nuevoApellido=None, nuevaEdad=None):
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
    def MostrarPacientesAtendidos(self):
        while True:
            print("""
                  1. Pacientes atendidos
                  2. Pacientes en proceso de atención
                  3. Pacientes en espera
                  """)
            opcion = int(input("Digite una opción: "))
            
            if opcion == 1:
                # Verificamos si hay pacientes atendidos
                if not self.pacientesAtendidos:
                    print("\nNo hay pacientes atendidos.")
                else:
                    print("\n-- Pacientes atendidos --")
                    print(f"{'Nombre':<20}{'Apellido':<20}{'Edad':<20}{'Identificación':<20}{'Estado':<20}")
                    for paciente in self.pacientesAtendidos:
                        print(f"{paciente.nombre:<20}{paciente.apellido:<20}{str(paciente.edad):<20}{paciente.identificacion:<20}{paciente.estado:<20}")
                break
            elif opcion == 2:
                # Verificamos si hay pacientes en proceso de atención
                if self.pacientesEnProceso.vacia():
                    print("\nNo hay pacientes en proceso de atención")
                else:
                    print("\n-- Pacientes en proceso de atención --")
                    print(f"{'Nombre':<20}{'Apellido':<20}{'Edad':<20}{'Identificación':<20}{'Estado':<20}")
                    for paciente in reversed(self.pacientesEnProceso):
                        print(f"{paciente.nombre:<20}{paciente.apellido:<20}{str(paciente.edad):<20}{paciente.identificacion:<20}{paciente.estado:<20}")
                break
            elif opcion == 3:
                # Verificamos si hay pacientes en espera
                if self.pacientesEnEspera.estaVacia():
                    print("\nNo hay pacientes en espera")
                else:
                    print("\n-- Pacientes en espera --")
                    print(f"{'Nombre':<20}{'Apellido':<20}{'Edad':<20}{'Identificación':<20}{'Estado':<20}")
                    nodoActual = self.pacientesEnEspera.primero
                    while nodoActual is not None:
                        paciente = nodoActual.dato
                        print(f"{paciente.nombre:<20}{paciente.apellido:<20}{str(paciente.edad):<20}{paciente.identificacion:<20}{paciente.estado:<20}")
                        nodoActual = nodoActual.siguiente
                break
            else:
                print("\nOpción no válida")
          
    # Método para cambiar el estado de un paciente
    def cambiarEstado(self, identificacion):
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
                        self.pacientesEnEspera.eliminar(existePaciente)
                        self.pacientesEnProceso.agregar(existePaciente)
                    elif nuevoEstado == "Atendido":
                        self.pacientesEnProceso.eliminar(existePaciente)
                        self.pacientesAtendidos.append(existePaciente)
                       
                        
                    print("\nEl estado del paciente ha sido actualizado.")
                    break
        else:
            print("\nPaciente no encontrado en urgencias.")