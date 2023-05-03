import minimalmodbus, serial, datetime, json

# Puerto disponibles

def validar_instrumento(puerto):
    try:
        instrument = minimalmodbus.Instrument(puerto, 3, minimalmodbus.MODE_RTU)
    except minimalmodbus.ModbusException as e:
        return None
    except serial.SerialException as e:
        return  None
    else:
        return instrument

# Crear diccionario

def crear_dic(instrument, keys, data_dict, dir):

    now = datetime.datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
    data_dict["fecha_hora"] = fecha_hora
            
    for i in range(len(dir)):
        try:
            if keys[i] == "battery_SOC" or keys[i] == "battery_current" or keys[i] == "load_status":
                var = instrument.read_register(dir[i], functioncode=4)
            else:
                var = instrument.read_register(dir[i], functioncode=4)/100
        except:
            var = ""
        data_dict[keys[i]] = var

# Diccionario vacio

def vacio(keys, data_dict):

    now = datetime.datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
    data_dict["fecha_hora"] = fecha_hora

    for i in range(len(keys)):
        data_dict[keys[i]] = ""

# Enviar diccionario

def enviar(ser, data_dict):
    json_data = json.dumps(data_dict)
    bytes_data = json_data.encode()
    ser.write(bytes_data)