from flask import Flask, render_template, request
from app.conexion import BaseDatos
import smtplib, ssl
from email.mime.text import MIMEText

instaciaBd = BaseDatos()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    # a simple page that says hello
    @app.route('/',methods=["GET","POST"])
    def inicio():
        
        info = {}
        if request.method == 'POST':
            id_funcionario = request.form["id_funcionario"]
            nombre_funcionario = request.form["nombre_funcionario"]
            apellido_funcionario = request.form["apellido_funcionario"]
            cedula_funcionario = request.form["cedula_funcionario"]
            telefono_funcionario = request.form["telefono_funcionario"]
            correo_funcionario = request.form["correo_funcionario"]
            cargo_funcionario = request.form["cargo_funcionario"]
            facultad_funcionario = request.form["facultad_funcionario"]


            if (id_funcionario == "" or nombre_funcionario == "" or apellido_funcionario == "" or cedula_funcionario == ""  
            or cargo_funcionario == "" or correo_funcionario == ""):
                info["error"] = "Campos vacios"
            elif len(telefono_funcionario) != 0 and len(telefono_funcionario) != 10:
                info["error"] = "El teléfono debe tener 10 caracteres o no estar vacio"
            else:
                resp = instaciaBd.agregar_funcionario((
                    id_funcionario,
                    cargo_funcionario,
                    facultad_funcionario,
                    nombre_funcionario,
                    apellido_funcionario,
                    cedula_funcionario,
                    telefono_funcionario,
                    correo_funcionario
                ))
                
                if resp == 1:
                    envia_desde = "bdortegav@correo.udistrital.edu.co"
                    msg = MIMEText(f'Bienvenido {nombre_funcionario} a Bd de prueba')

                    msg['Subject'] = 'Se registro satisfactoriamente en la BD!'
                    msg['From'] = 'BasesDeDatos1@basesdatos1.com'
                    msg['To'] = correo_funcionario


                    contrasena = "econkznvfjyphojt"
                    contexto = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
                        server.login(envia_desde, contrasena)
                        server.sendmail(envia_desde, correo_funcionario, msg.as_string())

                    info["success"] = "Funcionario creado correctamente"
                else:
                    info["error"] = resp
        
        cargos = []
        for cargo in instaciaBd.traer_cargos():
            cargos.append(cargo)
        
        facultades = []
        for facultad in instaciaBd.traer_facultad():
            facultades.append(facultad)
        

        info["cargos"]= cargos
        info["facultades"] = facultades
        return render_template('inicio.html', info=info)

    return app


if __name__ == "__main__":
    app_flask = create_app()
    app_flask.debug = True
    app_flask.run()