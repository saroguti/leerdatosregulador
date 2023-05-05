import time, serial, funciones

# Configuracion del dispositivo

ser = serial.Serial(port='COM10', baudrate=115200)

# Direcciones y claves

keys = ["array_current", "array_voltage", "array_power", "battery_voltage", "battery_current", "battery_SOC", 
        "battery_temp", "regulator_temp", "load_current", "load_voltage", "load_power", "load_status"]
      
dir = [0x3101, 0x3100, 0x3102, 0x331A, 0x331B, 0x311A, 
        0x3110, 0x3111, 0x310D, 0x310C, 0x310E, 0x3202]

# Crear diccionarios para los datos y el error

data_dict = {}

# Lectura de registros

while True:
    instrument = funciones.validar_instrumento(puerto='COM8')
    # Intenta crear llenar el diccionario con los datos de los registros
    if instrument == None:
        funciones.vacio(keys, data_dict)
        funciones.enviar(ser, data_dict)
        print("\nError.")
        time.sleep(10)
        continue
    try:
        instrument.serial.baudrate = 115200
        instrument.serial.timeout = 1

        funciones.crear_dic(instrument, keys, data_dict, dir)
        funciones.enviar(ser, data_dict)

        print("\nEnviando datos...")
        print("\n", data_dict)
        
        time.sleep(10)

    # Si existe un error envia un json con NC
    except Exception as e:
        funciones.vacio(keys, data_dict)
        funciones.enviar(ser, data_dict)
        print("\nError.")
        instrument.serial.close()
        time.sleep(10)
