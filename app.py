from flask_ngrok import run_with_ngrok
from flask import Flask
import wikipedia as w

from deeppavlov import build_model, configs
model_qa_ml = build_model(configs.squad.squad_bert_multilingual_freezed_emb, download=True)  

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
run_with_ngrok(app)   #starts ngrok when the app is run

#context = 'Hi, I am ananthaprakash. This is a general content. You have to provide a content to make the chatbot to answer for your questions. Good Luck'
context = ''
@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
  message = request.form['messageText'].encode('utf-8').lower().decode()
  global context
  #kernel now ready for use
  while True:
    if message == "quit":
      #exit()
      bot_response = "Bye Bye. Ended Successfully.\n LOL just kidding :). I am running in server. So, I won't stop :D"
    elif message == "hi":
      bot_response = "Hello, Please start asking the questions"
    elif message.find("!content")!=-1:
      #Write in notepad
      context = message[8:]
      with open("./context.txt","w") as cont:
        cont.write(context)
      bot_response = "Content Successfully Overwritten"
    elif (message.find("created")!=-1 and message.find("you")!=-1) or message.find("ananthaprakash")!=-1:
      bot_response = "I was created by SIH team for Military Purpose"
    else:
      bot_response = str(model_qa_ml([context],[message])[0][-1])
      if bot_response =="":
        context_temp = w.summary(message)
        bot_response = str(model_qa_ml([context_temp],[message])[0][-1])
    return jsonify({'status':'OK','answer':bot_response})
if __name__ == "__main__":
    app.run()
