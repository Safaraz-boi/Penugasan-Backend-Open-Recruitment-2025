# http_server.py
from flask import Flask, request, jsonify

from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

from lib_config import LibConfig
from lib_systems import LibSystems
from lib_postgresql import LibPostgreSQL

class HTTPServer:

    def __init__(self):
        self.app = Flask(__name__)

        LibSystems.readConfig()

        self.app.config["JWT_SECRET_KEY"] = LibConfig.JWT_KEY
        jwt = JWTManager(self.app)

        self.db = LibPostgreSQL(
            host=LibConfig.DB_HOST,
            dbname=LibConfig.DB_NAME,
            user=LibConfig.DB_USER,
            password=LibConfig.DB_PASS,
        )

        self.register_routes()

    def register_routes(self):
        
        @self.app.route('/')
        def index():
            return "Request not supported!"
        
        @self.app.route("/api/login_jwt", methods=["POST"])
        def login_jwt():

            try:
                if not request.is_json:
                    return jsonify({"error": "Request must be JSON"}), 400

                username = request.json.get("username")
                password = request.json.get("password")

                if username != LibConfig.JWT_USER or password != LibConfig.JWT_PASS:
                    return jsonify({"msg": "Bad credentials"}), 401

                token = create_access_token(identity=username)
                return jsonify(access_token=token)
            
            except Exception as e:
                LibSystems.write_daily_log(f"Error processing JSON request: {e}")
                return jsonify({"error": "Invalid JSON or internal server error", "details": str(e)}), 500
            finally:
                LibSystems.write_daily_log("Finished processing request.")
        
        @self.app.route("/api/check_jwt", methods=["GET"])
        @jwt_required()
        def check_jwt():
            user = get_jwt_identity()
            return jsonify(logged_in_as=user), 200

        @self.app.route("/api/list_mahasiswa", methods=["GET"])
        @jwt_required()
        def get_list_users():

            try:

                get_jwt_identity()

                LibSystems.write_daily_log(f"Get list mahasiswa data request received.")

                cur = self.db.get_cursor()
                cur.execute("SELECT * FROM mahasiswa;")
                users = cur.fetchall()
                cur.close()
                return jsonify(users)
             
            except Exception as e:
                LibSystems.write_daily_log(f"Error processing request: {e}")
                return jsonify({"error": "Invalid request or internal server error", "details": str(e)}), 500
            finally:
                LibSystems.write_daily_log("Finished processing request.")
        
        @self.app.route("/api/data_mahasiswa", methods=["POST"])
        @jwt_required()
        def get_data_users():

            try:
                nim = request.form.get("nim")

                LibSystems.write_daily_log(f"Check nim: {nim}")
                        
                if (len(nim) != 10) :
                    return jsonify({"error": "NIM harus 10 digit angka."}), 400
                    
                if (nim.isdigit() == False) :
                    return jsonify({"error": "Format NIM harus 10 digit angka."}), 400

                cur = self.db.get_cursor()
                cur.execute(
                    "SELECT * FROM mahasiswa WHERE nim = %s;", (nim,)
                )
                
                users = cur.fetchall()
                cur.close()
                return jsonify(users)

            except Exception as e:
                LibSystems.write_daily_log(f"Error processing request: {e}")
                return jsonify({"error": "Invalid request or internal server error", "details": str(e)}), 500
            finally:
                LibSystems.write_daily_log("Finished processing request.")    
        
        @self.app.route("/api/create_mahasiswa", methods=["POST"])
        @jwt_required()
        def create_user():

            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400

            try:
                data = request.get_json(force=False)

                LibSystems.write_daily_log(f"Received: {data}")
                    
                nim = data.get("nim")
                name = data.get("name")
                email = data.get("email")

                if (len(nim) == 0) or (len(name) == 0) or (len(email) < 0):
                    return jsonify({"error": "Masukkan NIM, Nama atau Email yang benar."}), 400
                
                if (len(nim) != 10) :
                    return jsonify({"error": "NIM harus 10 digit angka."}), 400
                
                if (nim.isdigit() == False) :
                    return jsonify({"error": "Format NIM harus 10 digit angka."}), 400
                
                if (len(name) < 5) :
                    return jsonify({"error": "Nama minimal 5 karakter."}), 400
                
                if (LibSystems.is_valid_email(email) == False) :
                    return jsonify({"error": "Masukkan email yang benar."}), 400

                cur = self.db.get_cursor()
                cur.execute(
                    "INSERT INTO mahasiswa (nim, name, email, status) VALUES (%s, %s, %s, 1) RETURNING nim;",
                    (nim, name, email)
                )

                if cur.rowcount == 0:
                    return jsonify({"error": "Data mahasiswa tidak dapat di masukkan."}), 404
                else:
                    self.db.commit()
                
                nim = cur.fetchone()["nim"]
                self.db.commit()
                cur.close()

                response_data = {
                    "status": "Sukses",
                    "nim": nim,
                    "name": name,
                    "name": email,
                    "message": "Data mahasiswa berhasil ditambahkan."
                }

                return jsonify(response_data), 200

            except Exception as e:
                LibSystems.write_daily_log(f"Error processing JSON request: {e}")
                return jsonify({"error": "Invalid JSON or internal server error", "details": str(e)}), 500
            finally:
                LibSystems.write_daily_log("Finished processing request.")

        @self.app.route("/api/update_mahasiswa", methods=["POST"])
        @jwt_required()
        def update_user():

            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400

            try:
                data = request.get_json(force=False)

                LibSystems.write_daily_log(f"Received: {data}")
                    
                nim = data.get("nim")
                name = data.get("name")
                email = data.get("email")
                status = data.get("status")

                if (len(nim) == 0) or (len(name) == 0) or (len(email) < 0):
                    return jsonify({"error": "Masukkan NIM, Nama atau Email yang benar."}), 400
                
                if (len(nim) != 10) :
                    return jsonify({"error": "NIM harus 10 digit angka."}), 400
                
                if (nim.isdigit() == False) :
                    return jsonify({"error": "Format NIM harus 10 digit angka."}), 400
                
                if (len(name) < 5) :
                    return jsonify({"error": "Nama minimal 5 karakter."}), 400
                
                if (LibSystems.is_valid_email(email) == False) :
                    return jsonify({"error": "Masukkan email yang benar."}), 400
                
                if (status not in [0,1]) :
                    status=1

                cur = self.db.get_cursor()
                cur.execute(
                    "UPDATE mahasiswa SET name=%s, email=%s, status=%s WHERE nim=%s;",
                    (name, email, status, nim)
                )

                self.db.commit()
                cur.close()

                response_data = {
                    "status": "Sukses",
                    "nim": nim,
                     "name": name,
                     "name": email,
                    "name": status,
                    "message": "Data mahasiswa berhasil diubah."
                }

                return jsonify(response_data), 200

            except Exception as e:
                LibSystems.write_daily_log(f"Error processing JSON request: {e}")
                return jsonify({"error": "Invalid JSON or internal server error", "details": str(e)}), 500
            finally:
                LibSystems.write_daily_log("Finished processing request.")

        @self.app.route("/api/remove_mahasiswa", methods=["POST"])
        @jwt_required()
        def remove_user():
            
            try:
                nim = request.form.get("nim")

                LibSystems.write_daily_log(f"Remove nim: {nim}")
                    
                if (len(nim) != 10) :
                    return jsonify({"error": "NIM harus 10 digit angka."}), 400
                
                if (nim.isdigit() == False) :
                    return jsonify({"error": "Format NIM harus 10 digit angka."}), 400
                
                cur = self.db.get_cursor()
                cur.execute(
                    "DELETE from mahasiswa WHERE nim = %s;", (nim,)
                )
                
                if cur.rowcount == 0:
                    return jsonify({"error": "NIM tidak ditemukan."}), 404
                else:
                    self.db.commit()
                
                cur.close()
                
                response_data = {
                    "status": "Sukses",
                    "nim": nim,
                    "message": "Data mahasiswa berhasil dihapus."
                }

                return jsonify(response_data), 200

            except Exception as e:
                LibSystems.write_daily_log(f"Error processing request: {e}")
                return jsonify({"error": "Invalid request or internal server error", "details": str(e)}), 500
            finally:
                LibSystems.write_daily_log("Finished processing request.")

    def run(self):
        self.app.run(debug=True, host=LibConfig.SERVER_IP, port=LibConfig.SERVER_PORT)

if __name__ == '__main__':
    HTTPServer().run()