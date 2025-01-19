from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

#GREETING_INPUTS = ["నమస్కారం", "హలో", "హాయ్", "నమస్తే", "వందనాలు"]

@app.route('/')
def index():
    return render_template('voice.html')

@app.route('/voice_query', methods=['POST'])
def voice_query():
    data = request.get_json()
    query = data.get('query', '').lower()

    # Sample responses for Telugu queries
    if 'హలో' in query :
        answer = 'హలో! నేను మీకు ఎలా సహాయం చేయగలను?'
    elif 'సమయం' in query:
        answer = f'ఆసుపత్రి సమయాలు ఉదయం 9.30 నుండి సాయంత్రం 5 గంటల వరకు'
    elif 'అంబులెన్స్' in query:
        answer = f'అంబులెన్స్ సేవ ఎల్లప్పుడూ అందుబాటులో ఉంటుంది . అంబులెన్స్ నంబర్లు, ఉదయం 9032420992, రాత్రి 8008103804'
    elif 'ఎక్కడ' in query:
        answer=f'గేట్ నంబర్ 2 నుండి నేరుగా వెళ్లండి, మీ గమ్యం ఎడమ వైపున ఉంది'
    elif 'బై' in query:
        answer=f'మా సేవను ఉపయోగించినందుకు ధన్యవాదాలు'
    else:
        answer = 'క్షమించండి, నేను ఆ ప్రశ్న అర్థం చేసుకోలేకపోయాను.'

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

