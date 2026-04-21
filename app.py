from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host":     "localhost",
    "database": "parkup_db",
    "user":     "postgres",
    "password": "#Bharath01usa",
    "port":     5432
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


# READ - Get all parking spots
@app.route('/spots', methods=['GET'])
def get_spots():
    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT SpotID as spotid, LotID as lotid, SpotLabel as spotlabel, SpotType as spottype, IsActive as isactive, Status as status FROM ParkingSpot ORDER BY SpotID;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# CREATE - Insert a new parking spot
@app.route('/spots', methods=['POST'])
def create_spot():
    data = request.get_json()
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO ParkingSpot (SpotID, LotID, SpotLabel, SpotType, IsActive, Status) VALUES (%s, %s, %s, %s, %s, %s) RETURNING SpotID;",
            (data['spotid'], data['lotid'], data['spotlabel'], data['spottype'], data['isactive'], data['status'])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"spotid": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE - Edit an existing parking spot
@app.route('/spots/<int:spot_id>', methods=['PUT'])
def update_spot(spot_id):
    data = request.get_json()
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute(
            "UPDATE ParkingSpot SET LotID=%s, SpotLabel=%s, SpotType=%s, IsActive=%s, Status=%s WHERE SpotID=%s;",
            (data['lotid'], data['spotlabel'], data['spottype'], data['isactive'], data['status'], spot_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE - Remove a parking spot
@app.route('/spots/<int:spot_id>', methods=['DELETE'])
def delete_spot(spot_id):
    try:
        conn = get_conn()
        cur  = conn.cursor()
        cur.execute("DELETE FROM ParkingSpot WHERE SpotID=%s;", (spot_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
