import oracledb
import os
from app.config import Config
oracledb.init_oracle_client(lib_dir="C:/app/bryda/product/21c/dbhomeXE/bin")
os.environ["NLS_LANG"] = "SPANISH_SPAIN.UTF8"

class BaseDatos:
    def __init__(self):
        self.__connection = oracledb.connect(
            user=Config.usuario,
            password=Config.password,
            dsn=Config.dns,
            encoding='AL16UTF16', nencoding='AL16UTF16')

        self.__cursor = self.__connection.cursor()
        print("Successfully connected to Oracle Database")        


    def agregar_funcionario(self, row):
        try:
            self.__cursor.execute("INSERT INTO FUNCIONARIO (IDFUNCIONARIO, IDCARGO, IDFACULTAD, NOMBREFUNCIONARIO, APELLIDOFUNCIONARIO,\
                                CEDULAFUNCIONARIO, TEFFUNCIONARIO, CORREOFUNCIONARIO) VALUES(:1,:2,:3,:4,:5,:6,:7,:8)",row)
            filas_afectadas = self.__cursor.rowcount
            self.__connection.commit()
            return filas_afectadas
        except oracledb.IntegrityError as err:            
            if "PK_FUNCIONARIO" in str(err):
                return "El id ya está en uso, seleccione otro"
            elif "PROMO2022.SYS_C008408" in str(err):
                return "La cédula ya está en uso, seleccione otra"
            elif "PROMO2022.SYS_C008412" in str(err):                
                return "El correo ya está en uso, seleccione otro"
            else:
                return str(err)
        except oracledb.DatabaseError as err:
            errors ,= err.args
            if errors.code == 12899:
                if "NOMBREFUNCIONARIO" in str(err):
                    return "El valor es demasiado grande para el nombre"
                elif "APELLIDOFUNCIONARIO" in str(err):
                    return "El valor es demasiado grande para el apellido"
                elif "IDFUNCIONARIO" in str(err):
                    return "El valor es demasiado grande para el id"
                elif "CEDULAFUNCIONARIO" in str(err):
                    return "El valor es demasiado grande para el cedula"
                elif "TEFFUNCIONARIO" in str(err):
                    return "El valor es demasiado grande para el telefono"
                elif "CORREOFUNCIONARIO" in str(err):
                    return "El valor es demasiado grande para el correo"                    
                else:
                    return str(err)
            else:
                return str(err)
            
        



    def traer_cargos(self):
        rows = self.__cursor.execute("SELECT IDCARGO,NOMBRECARGO FROM CARGO")        
        return rows

    def traer_facultad(self):
        rows = self.__cursor.execute("SELECT IDFACULTAD,NOMBREFACULTAD FROM FACULTAD")        
        return rows
        