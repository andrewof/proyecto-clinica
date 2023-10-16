from urgencias import ClinicaUrgencias

# Menú para poder interactuar con el programa
def menu():
    urgencias = ClinicaUrgencias()
    
    while True:
        print("""\n
                 -- Menú --
              1. Registrar paciente
              2. Actualizar datos del paciente
              3. Mostrar pacientes en espera/proceso/atendidos
              4. Cambiar estado del paciente
              5. Salir
              """)
        opcion = int(input("Digite una opción: "))
        
        print()
        if opcion == 1:
            print("Datos del paciente")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            identificacion = input("Identificación: ")
            urgencias.registrarPaciente(nombre, apellido, edad, identificacion)
        elif opcion == 2:
            print("Digite la identificación del paciente a actualizar sus datos")
            identificacion = input("Identificación: ")
            urgencias.actualizarPaciente(identificacion)
        elif opcion == 3:
            urgencias.MostrarPacientesAtendidos()
        elif opcion == 4:
            print("Digite la identificación del paciente para cambiar su estado")
            identificacion = input("Identificación: ")
            urgencias.cambiarEstado(identificacion)
        elif opcion == 5:
            print("\nPrograma finalizado.")
            break
        else:
            print("\nOpción no válida.")
            
# Para poder correr el programa desde la terminal         
if __name__ == "__main__":
    menu()               