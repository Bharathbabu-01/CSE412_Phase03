from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# database connection info
db_host = "localhost"
db_name = "parkup_db"
db_user = "postgres"
db_pass = "------------- Enter Your Password Here, Same Password as Your PG Admin for Testing It -------------"
db_port = 5432

def get_conn():
    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass, port=db_port)
    return conn

# get all parking spots
@app.route('/spots', methods=['GET'])
def get_spots():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT SpotID, LotID, SpotLabel, SpotType, IsActive, Status FROM ParkingSpot ORDER BY SpotID;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for r in rows:
        spot = {
            "spotid": r[0],
            "lotid": r[1],
            "spotlabel": r[2],
            "spottype": r[3],
            "isactive": r[4],
            "status": r[5]
        }
        result.append(spot)

    return jsonify(result)

# add new parking spot
@app.route('/spots', methods=['POST'])
def create_spot():
    data = request.get_json()
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ParkingSpot (SpotID, LotID, SpotLabel, SpotType, IsActive, Status) VALUES (%s, %s, %s, %s, %s, %s);",
            (data['spotid'], data['lotid'], data['spotlabel'], data['spottype'], data['isactive'], data['status'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"spotid": data['spotid']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# update a parking spot
@app.route('/spots/<int:spot_id>', methods=['PUT'])
def update_spot(spot_id):
    data = request.get_json()
    try:
        conn = get_conn()
        cur = conn.cursor()
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

# delete a parking spot
@app.route('/spots/<int:spot_id>', methods=['DELETE'])
def delete_spot(spot_id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM ParkingSpot WHERE SpotID=%s;", (spot_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
