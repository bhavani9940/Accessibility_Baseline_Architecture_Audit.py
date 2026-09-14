from flask import Flask, jsonify

app = Flask(__name__)

@app.get('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'service': 'server'
    })

@app.get('/api/feature')
def feature():
    return jsonify({
        'message': 'First vertical feature is working'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)