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
        self.medicamentosRecetados = []
        
    def establecerServicio(self, servicio):
        if servicio not in self.servicios:
            self.servicios.append(servicio)
        
    def establecerMedicamento(self, medicamento):
        self.medicamentos.append(medicamento)
        if "Cuidado intermedio" in self.servicios:
            self.medicamentosRecetados.append(medicamento)
    
class Urgencia:
    def __init__(self):
        self.pacientes = Cola() # Cola para guardar los pacientes para guardar por orden de llegada
        self.pacientesAtendidos = [] # Lista simple
        self.pacientesEnEspera = listaDoble() # Lista doble para los pacientes en espera
        self.pacientesEnProceso = Pila() # Pila para los pacientes que están en proceso
        self.serviciosClinica = ["Cirugia", "Medicina interna", "Hospitalización", "Cuidado intermedio", "Diagnóstico"]
        self.medicamentosDisponibles = []
    
    # Método para registrar los pacientes
    def registrarPaciente(self, nombre, apellido, edad, identificacion, eps, servicio=None):
        estado = "En espera"
        
        # Verificamos si el paciente está registrado
        for paciente in self.pacientes:
            if paciente.identificacion == identificacion:
                print("\nEste paciente ya está registrado en la sala de urgencias.")
                return
        
        # Si no está registrado, creamos una variable de tipo Paciente y pasamos los datos del paciente   
        nuevoPaciente = Paciente(nombre, apellido, edad, identificacion, eps, estado)
        
        print("\nServicios disponibles")
        for i, servicio in enumerate(self.serviciosClinica, 1):
            print(f"{i}. {servicio}")
        try:
            opcion = int(input("Opción: "))
            if 1 <= opcion <= len(self.serviciosClinica):
                servicio = self.serviciosClinica[opcion - 1]
                nuevoPaciente.establecerServicio(servicio)
                if servicio in ["Cirugia", "Hospitalización"]:
                    estado = "En proceso de atención"
                    self.pacientesEnProceso.agregar(nuevoPaciente)
                elif servicio in ["Medicina interna", "Cuidado intermedio"]:
                    estado = "Atendido"
                    self.pacientesAtendidos.append(nuevoPaciente)
                    
                    if servicio == "Cuidado intermedio":
                        self.asignarMedicamentoCuidadoIntermedio(nuevoPaciente)
                elif servicio == "Diagnóstico":
                    estado = "En espera"
                    self.pacientesEnEspera.insertarFinal(nuevoPaciente)
                print(f"\nEl servicio '{servicio}' fue asignado con éxito al paciente '{nuevoPaciente.nombre} {nuevoPaciente.apellido}'")
            else:
                print("\nOpción no válida.")
        except ValueError:
            print("\nOpción no válida.")
        
        nuevoPaciente.estado = estado
        
        self.pacientes.agregar(nuevoPaciente)
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
                while True:
                    nuevaEdadInput = input("Nueva edad: ")
                    
                    if nuevaEdadInput == "":
                        break
                    
                    try:
                        nuevaEdad = int(nuevaEdadInput)
                        break
                    except ValueError:
                        print("\nLa edad no puede ser una cadena.")
                nuevaEps = input("Nueva eps: ")
                
                if nuevoNombre != "":
                    paciente.nombre = nuevoNombre
                if nuevoApellido != "":
                    paciente.apellido = nuevoApellido
                if nuevaEdad is not None:
                    paciente.edad = nuevaEdad
                if nuevaEps != "":
                    paciente.eps = nuevaEps
                
                print("\nDatos del paciente actualizados con éxito.")
                encontrado = True
                break
        if not encontrado:
            print("\nPaciente no encontrado en urgencias.")
    
    def registrarMedicamento(self, codigo, nombre, existencia):
        medicamentoNuevo = {"codigo": codigo, "nombre": nombre, "existencia": existencia}
        self.medicamentosDisponibles.append(medicamentoNuevo)
        print(f"\n¡Medicamento {nombre} registrado con éxito!")
        
    def asignarServicio(self, identificacion):
        paciente = self.buscarPaciente(identificacion)
        
        if paciente:
            if paciente.estado == "Atendido":
                print("\nNo se puede cambiar el servicio de un paciente ya atendido")
                return 
            
            print("\nServicios disponibles")
            for i, servicio in enumerate(self.serviciosClinica, 1):
                print(f"{i}. {servicio}")
            try:
                opcion = int(input("Opción: "))
                if 1 <= opcion <= len(self.serviciosClinica):
                    nuevoServicio = self.serviciosClinica[opcion - 1]
                    
                    if nuevoServicio not in paciente.servicios:
                        paciente.servicios = []
                        if paciente.estado == "En espera":
                            self.pacientesEnEspera.eliminar(paciente)
                        elif paciente.estado == "En proceso de atención":
                            self.pacientesEnProceso.eliminar(paciente)
                        elif paciente.estado == "Atendido":
                            self.pacientesAtendidos.remove(paciente)
                            
                        paciente.establecerServicio(nuevoServicio)
                        if nuevoServicio in ["Cirugia", "Hospitalización"]:
                            paciente.estado = "En proceso de atención"
                            self.pacientesEnProceso.agregar(paciente)
                        elif nuevoServicio in ["Medicina interna", "Cuidado intermedio"]:
                            paciente.estado = "Atendido"
                            self.pacientesAtendidos.append(paciente)
                            if nuevoServicio == "Cuidado intermedio":
                                self.asignarMedicamentoCuidadoIntermedio(paciente)
                        elif nuevoServicio == "Diagnóstico":
                            paciente.estado = "En espera"
                            self.pacientesEnEspera.insertarFinal(paciente)
                        
                        print(f"\nEl servicio '{nuevoServicio}' fue asignado con éxito al paciente '{paciente.nombre} {paciente.apellido}'")
                    else:
                        print("\nEl paciente ya tiene asignado ese servicio.")
                else:
                    print("\nOpción no válida.")
            except ValueError:
                print("\nOpción no válida.")
        else:
            print("\nPaciente no encontrado en urgencias.")
            
    def asignarMedicamentoCuidadoIntermedio(self, paciente):
        if "Cuidado intermedio" in paciente.servicios:
            codigoMedicamento = input("\nCódigo medicamento: ")
            medicamento = self.buscarMedicamento(codigoMedicamento)
            if not medicamento:
                # Si el medicamento no existe
                print("\nEl medicamento no existe. Por favor registrarlo.")
                nombreMedicamento = input("Nombre medicamento: ")
                while True:
                    try:
                        existenciaMedicamento = int(input("Existencia medicamento: "))
                        break
                    except ValueError:
                        print("\nLas existencias deben ser en números.")
                medicamento = {"codigo": codigoMedicamento, "nombre": nombreMedicamento, "existencia": existenciaMedicamento}
            nuevoMedicamento = Medicamento(medicamento['codigo'], medicamento['nombre'], medicamento['existencia'])
            paciente.establecerMedicamento(nuevoMedicamento)
            print(f"\nMedicamento '{nuevoMedicamento.nombre}' asignado con éxito al paciente '{paciente.nombre} {paciente.apellido}'")
            medicamento['existencia'] -= 1
        
    def buscarMedicamento(self, codigo):
        for medicamento in self.medicamentosDisponibles:
            if medicamento['codigo'] == codigo:
                return medicamento
        return None
    
    def buscarPaciente(self, identificacion):
        for paciente in self.pacientes:
            if paciente.identificacion == identificacion:
                return paciente
        return None
    
    # Método para mostrar los datos de los pacientes en tablas
    def tabla(self, pacientes):
        if not pacientes:
            print("\nNo hay pacientes actualmente")
            return
        
        anchoColumna = 16
        
        if not pacientes or (hasattr(pacientes, 'vacia') and pacientes.vacia()):
            print("\nNo hay pacientes actualmente.")
            return
        
        if hasattr(pacientes, 'item') and not pacientes.vacia():
            pacientes = list(pacientes)
        
        encabezado = f"{'Nombre':^{anchoColumna}} {'Apellido':^{anchoColumna}} {'Edad':^{anchoColumna}} {'Identificación':^{anchoColumna}} {'EPS':^{anchoColumna}} {'Estado':^{anchoColumna}} {'Servicios':^{anchoColumna}}"
        print(encabezado)
        print("-"*len(encabezado))
        
        for paciente in pacientes:
            servicios = ", ".join(paciente.servicios)
            fila = f"{paciente.nombre:^{anchoColumna}} {paciente.apellido:^{anchoColumna}} {str(paciente.edad):^{anchoColumna}} {paciente.identificacion:^{anchoColumna}} {paciente.eps:^{anchoColumna}} {paciente.estado:^{anchoColumna}} {servicios:^{anchoColumna}}"
            print(fila)
    
    def mostrarPacientesEnEspera(self):
        print("\nPacientes en espera")
        nodoActual = self.pacientesEnEspera.primero
        pacientes = []
        while nodoActual is not None:
            paciente = nodoActual.dato
            pacientes.append(paciente)
            nodoActual = nodoActual.siguiente
        self.tabla(pacientes)
            
    def mostrarPacientesProcesoAtencion(self):
        print("\nPacientes en proceso de Atención")
        self.tabla(self.pacientesEnProceso)
            
    def mostrarPacientesAtendidos(self):
        print("\nPacientes atendidos")
        
        if not self.pacientesAtendidos:
            print("\nNo hay pacientes actualmente.")
            return
        
        for paciente in self.pacientesAtendidos:
            self.mostrarDatosPacienteMedicinaInterna(paciente)
        
    def mostrarDatosPacienteMedicinaInterna(self, paciente):
        encabezado = f"{'Nombre':^16} {'Apellido':^16} {'Edad':^16} {'Identificación':^16} {'EPS':^16} {'Estado':^16} {'Servicios':^16}"
        
        servicios = ", ".join(paciente.servicios)
        medicamentoRecetado = ", ".join([medicamento.nombre for medicamento in paciente.medicamentosRecetados])
        fila = f"{paciente.nombre:^16} {paciente.apellido:^16} {str(paciente.edad):^16} {paciente.identificacion:^16} {paciente.eps:^16} {paciente.estado:^16} {servicios:^16}"
        
        if "Cuidado intermedio" in paciente.servicios:
            medicamentoRecetado = ", ".join([medicamento.nombre for medicamento in paciente.medicamentosRecetados])
            encabezado += f" {'Medicamentos Recetados':^25}"
            fila += f" {medicamentoRecetado:^25}"
        
        print(encabezado)
        print("-"*len(encabezado))
        print(fila)
        
        if "Medicina interna" in paciente.servicios:
            print(f"\nEl paciente '{paciente.nombre} {paciente.apellido}' fue remitido a consulta prioritaria a la EPS '{paciente.eps}'\n")
        
                
    def menuParaMostrarPacientes(self):
        while True:
            print("""
                     -- Mostrar pacientes --
                  1. Pacientes en espera
                  2. Pacientes en proceso de atención
                  3. Pacientes atendidos
                  4. Menú principal
                  """)
            try: 
                opcion = int(input("Opción: "))
            except ValueError:
                print("\nLa opción tiene que ser un número.")
                continue

            if opcion == 1:
                self.mostrarPacientesEnEspera()
                break
            elif opcion == 2:
                self.mostrarPacientesProcesoAtencion()
                break
            elif opcion == 3:
                self.mostrarPacientesAtendidos()
                break
            elif opcion == 4:
                break
            else:
                print("\nOpción no válida")
             
    def menu(self):
        while True:
            print("""\n
                    -- Menú --
                1. Registrar paciente
                2. Mostrar pacientes en espera/proceso/atendidos
                3. Actualizar datos del paciente
                4. Registrar medicamento
                5. Cambiar servicios
                6. Salir
                """)
            try:
                opcion = int(input("Digite una opción: "))
            except ValueError:
                print("\nLa opción tiene que ser un número.")
                continue
            
            print()
            if opcion == 1:
                print("DATOS DEL PACIENTE")
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                while True:
                    try:
                        edad = int(input("Edad: "))
                        break
                    except ValueError:
                        print("\nLa edad no puede ser una cadena")
                identificacion = input("Identificación: ")
                eps = input("EPS: ")
                self.registrarPaciente(nombre, apellido, edad, identificacion, eps)
            elif opcion == 2:
                self.menuParaMostrarPacientes()
            elif opcion == 3:
                print("Digite la identificación del paciente para actualizar sus datos")
                identificacion = input("Identificación: ")
                self.actualizarPaciente(identificacion)
            elif opcion == 4:
                codigoMedicamento = input("Código: ")
                nombreMedicamento = input("Nombre: ")
                while True:
                    try:
                        existenciaMedicamento = int(input("Existencias: "))
                        break
                    except ValueError:
                        print("\nLas exitencias deben ingresarse en números.")
                self.registrarMedicamento(codigoMedicamento, nombreMedicamento, existenciaMedicamento)
            elif opcion == 5:
                print("Digite la identificación para cambiar los servicios del paciente")
                identificacion = input("Identificación: ")
                self.asignarServicio(identificacion)
            elif opcion == 6:
                break
            else:
                print("\nOpción no válida")