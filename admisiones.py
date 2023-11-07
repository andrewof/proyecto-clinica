from estructuras import ListaDobleEnlazada as listaDoble
from estructuras import Pila
from estructuras import Cola

class ServicioClinica:
    def __init__(self, nombre):
        self.nombre = nombre
        
class Medicamento:
    def __init__(self, codigo, nombre, existencia):
        self.codigo = codigo
        self.nombre = nombre 
        self.existencia = existencia

class Paciente:
    def __init__(self, nombre, apellido, edad, identificacion, eps, estado):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.identificacion = identificacion
        self.eps = eps
        self.estado = estado
        self.servicios = [] # Servicios asignados al paciente
        self.medicamentos = [] # Medicamento asignado al paciente
        
    def establecerServicio(self, servicio):
        self.servicios.append(servicio)
        
    def establecerMedicamento(self, medicamentos):
        self.medicamentos.append(medicamentos)
    
class Admisiones:
    def __init__(self):
        self.pacientes = Cola() # Cola para guardar los pacientes para guardar por orden de llegada
        self.pacientesAtendidos = [] # Lista simple
        self.pacientesEnEspera = listaDoble() # Lista doble para los pacientes en espera
        self.pacientesEnProceso = Pila() # Pila para los pacientes que están en proceso
        self.serviciosClinica = ["Cirugia", "Medicina interna", "Hospitalización", "Cuidado intermedio", "Diagnóstico"]
        self.medicamentosDisponibles = []
    
    # Método para registrar los pacientes
    def registrarPaciente(self, nombre, apellido, edad, identificacion, eps):
        estado = "En espera"
        
        # Verificamos si el paciente está registrado
        for paciente in self.pacientes:
            if paciente.identificacion == identificacion:
                print("\nEste paciente ya está registrado en la sala de urgencias.")
                return
        
        # Si no está registrado, creamos una variable de tipo Paciente y pasamos los datos del paciente   
        nuevoPaciente = Paciente(nombre, apellido, edad, identificacion, eps, estado)
        self.pacientes.agregar(nuevoPaciente)
        self.pacientesEnEspera.insertarFinal(nuevoPaciente)
        print("\nPaciente registrado exitosamente.")
    
    # Método para actualizar los datos de un paciente
    def actualizarPaciente(self, identificacion, nuevoNombre=None, nuevoApellido=None, nuevaEdad=None, nuevaEps=None):
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
                nuevaEps = input("Nueva eps: ")
                
                if nuevoNombre != "":
                    paciente.nombre = nuevoNombre
                if nuevoApellido != "":
                    paciente.apellido = nuevoApellido
                if nuevaEdad != "":
                    paciente.edad = nuevaEdad
                if nuevaEps != "":
                    paciente.eps = nuevaEps
                
                print("\nDatos del paciente actualizados con éxito.")
                encontrado = True
                break
        if not encontrado:
            print("\nPaciente no encontrado en urgencias.")
          
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
            
    def eliminarPaciente():
        pass
    
    def registrarMedicamento(self, codigo, nombre, existencia):
        medicamentoNuevo = {"codigo": codigo, "nombre": nombre, "existencia": existencia}
        self.medicamentosDisponibles.append(medicamentoNuevo)
        print(f"\n¡Medicamento {nombre} registrado con exito!")
        
    def asignarServicio(self, identificacion):
        existePaciente = None
        for paciente in self.pacientes:
            if paciente.identificacion == identificacion:
                existePaciente = paciente
                break
        
        if existePaciente:
            print("\nServicios disponibles")
            for i, servicio in enumerate(self.serviciosClinica, 1):
                print(f"{i}. {servicio}")
                
            while True:
                try:
                    opcion = int(input("Seleccione el servicio a asignar: "))
                    if 1 <= opcion <= len(self.serviciosClinica):
                        servicio = self.serviciosClinica[opcion - 1]
                        existePaciente.establecerServicio(servicio)
                        
                        if servicio in ["Cirugia", "Hospitalización"]:
                            self.pacientesEnProceso.agregar(existePaciente)
                        elif servicio in ["Medicina interna", "Cuidado intermedio"]:
                            self.pacientesAtendidos.append(existePaciente)
                        elif servicio == "Diagnostico":
                            self.pacientesEnEspera.insertarFinal(existePaciente)
                         
                        print(f"\nEl servicio {servicio} fue asignado al paciente {existePaciente.nombre} {existePaciente.apellido}")   
                        break 
                    else:
                        print("\nOpción no válida")
                except ValueError:
                    print("\nOpción no válida")
        else:
            print("\nPaciente no encontrado en urgencias.") 
            
    def asignarMedicamento(self, identificacion, codigoMedicamento):
        existePaciente = None
        for paciente in self.pacientes:
            if paciente.identificacion == identificacion:
                existePaciente = paciente
                break
        
        if existePaciente:
            if existePaciente.estado == "Atendido" and self.gradoUrgencia(existePaciente) == "De alta con Tratamiento":
                codigoMedicamento = str(codigoMedicamento)
                medicamento = self.buscarMedicamento(codigoMedicamento)
                
                if medicamento:
                    existePaciente.establecerMedicamento(medicamento)
                    print(f"\nMedicamento {medicamento['nombre']} asignado al paciente {existePaciente.nombre} {existePaciente.apellido}")
                    medicamento['existencia'] -= 1
                else:
                    print("\nMedicamento no encontrado")
            elif self.gradoUrgencia(existePaciente) == "De alta por Consulta Prioritaria":
                print(f"\nEl paciente será remitido a la EPS {existePaciente.eps}")
            else:
                print("\nNo se puede asignar medicamento a este paciente")
        else:
            print("\nPaciente no encontrado en urgencias.")
                
        
    def buscarMedicamento(self, codigo):
        for medicamento in self.medicamentosDisponibles:
            if medicamento['codigo'] == codigo:
                return medicamento
        return None
    
    def gradoUrgencia(self, paciente):
        servicioPaciente = paciente.servicios
        
        if "Cirugia" in servicioPaciente and "Hospitalización" in servicioPaciente:
            return "Admitido a urgencias"
        elif "Cuidado intermedio" in servicioPaciente:
            return "De alta con Tratamiento"
        elif "Medicina interna" in servicioPaciente:
            return "De alta por Consulta Prioritaria"
        elif "Diagnostico" in servicioPaciente:
            return "Esperando diagnostico"
        else:
            return "No se puede determinar el grado de la urgencia"
    
    def mostrarPacientesEnEspera(self):
        print("\nPacientes en espera")
        for paciente in self.pacientesEnEspera:
            servicios = ", ".join(paciente.servicios)
            print(f"Nombre: {paciente.nombre} Apellido: {paciente.apellido} Edad: {paciente.edad} Identificación: {paciente.identificacion} Estado: {paciente.estado} Servicios: {servicios} Grado urgencia: Admitido a urgencias")
            
    def mostrarPacientesProcesoAtencion(self):
        print("\nPacientes en proceso de Atención")
        for paciente in self.pacientesEnProceso:
            servicios = ", ".join(paciente.servicios)
            print(f"Nombre: {paciente.nombre} Apellido: {paciente.apellido} Edad: {paciente.edad} Identificación: {paciente.identificacion} Estado: {paciente.estado} Servicios: {servicios} Grado urgencia: Admitido a urgencias")
            
    def mostrarPacientesAtendidos(self):
        print("\nPacientes atendidos")
        for paciente in self.pacientesAtendidos:
            servicios = ", ".join(paciente.servicios)
            gradoUrgencia = self.gradoUrgencia(paciente)
            print(f"Nombre: {paciente.nombre} Apellido: {paciente.apellido} Edad: {paciente.edad} Identificación: {paciente.identificacion} Estado: {paciente.estado} Servicios: {servicios} Grado urgencia: {gradoUrgencia}")
            if gradoUrgencia == "De alta con Tratamiento":
                medicamento = ", ".join([medicamento.nombre for medicamento in paciente.medicamentos])
                print(f"Medicamento asignados {medicamento}")
            elif gradoUrgencia == "De alta por Consulta Prioritaria":
                print(f"El paciente será remitido a la EPS {paciente.eps}")
                
    def menuParaMostrarPacientes(self):
        while True:
            print("""
                     -- Mostrar pacientes --
                  1. Pacientes en espera
                  2. Pacientes en proceso de atención
                  3. Pacientes atendidos
                  4. Salir
                  """)
            opcion = int(input("Opción: "))

            if opcion == 1:
                self.mostrarPacientesEnEspera()
            elif opcion == 2:
                self.mostrarPacientesProcesoAtencion()
            elif opcion == 3:
                self.mostrarPacientesAtendidos()
            elif opcion == 4:
                break
            else:
                print("\nOpción no válida")
             
    def menu(self):
        while True:
            print("""\n
                    -- Menú --
                1. Registrar paciente
                2. Actualizar datos del paciente
                3. Mostrar pacientes en espera/proceso/atendidos
                4. Cambiar estado del paciente
                5. Registrar medicamento
                6. Asignar medicamento
                7. Asignar servicio
                8. Salir
                """)
            opcion = int(input("Digite una opción: "))
            
            print()
            if opcion == 1:
                print("DATOS DEL PACIENTE")
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                edad = int(input("Edad: "))
                identificacion = input("Identificación: ")
                eps = input("Eps: ")
                
                while True:
                    print("\nServicios disponibles")
                    for i, servicio in enumerate(self.serviciosClinica, 1):
                        print(f"{i}. {servicio}")
                    try:
                        opcion = int(input("Opción: "))
                        if 1 <= opcion <= len(self.serviciosClinica):
                            servicio = self.serviciosClinica[opcion - 1]
                            break
                        else:
                            print("\nOpción no válida")
                    except ValueError:
                        print("\nOpción no válida. Ingresa un número")
                self.registrarPaciente(nombre, apellido, edad, identificacion, eps)
                self.asignarServicio(identificacion, servicio)
            elif opcion == 2:
                print("Digite la identificación del paciente a actualizar sus datos")
                identificacion = input("Identifición: ")
                self.actualizarPaciente(identificacion)
            elif opcion == 3:
                self.menuParaMostrarPacientes()
            elif opcion == 4:
                print("Digite la identificación del paciente para cambiar su estado")
                identificacion = input("Identificación: ")
                self.cambiarEstado(identificacion)
            elif opcion == 5:
                codigo = input("Código: ")
                nombre = input("Nombre: ")
                existencia = int(input("Existencias: "))
                self.registrarMedicamento(codigo, nombre, existencia)
            elif opcion == 6:
                identificacion = input("Identificación: ")
                codigoMedicamento = int(input("Código medicamento: "))
                self.asignarMedicamento(identificacion, codigoMedicamento)
            elif opcion == 7:
                identificacion = input("Identificación: ")
                self.asignarServicio(identificacion)
            else:
                print("\nOpción no válida")
    