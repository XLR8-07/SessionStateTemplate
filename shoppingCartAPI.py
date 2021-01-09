import json
import uuid
import flask
from os import path
from flask import Flask, jsonify, request

#intialize the Flash app
app = Flask(__name__)

#Test URL
@app.route('/',methods = ['GET','POST'])
def index():
    return jsonify({"welcome":"Welcome to the Shopping Cart API"})

#ADD CART
@app.route('/cart/add/<productName>',methods = ['POST'])
def addCart(productName):
    response = flask.Response()
    if request.headers.get('session-id'):
        sessionID =  request.headers['session-id']
        fileName =  str(sessionID)+'.json'
        if(path.exists(fileName)):
            cart =  open(fileName,'r')
            data = json.load(cart)
            cart.close()
            if productName in data:
                data[productName] = data[productName] + 1
                cart = open(fileName,'w')
                print(data)
                json.dump(data,cart)
                response.headers['session-id'] = sessionID
                return response
            else:
                data[productName] = 1
                cart = open(fileName,'w')
                json.dump(data,cart)
                print(data)
                response.headers['session-id'] = sessionID
                return response 
        else:
            print("No SESSION EXISTS")  
            return jsonify({"error":"No Session exists"})
        
    else:
        #Intiation of a session
        sessionID = uuid.uuid1()
        fileName = str(sessionID) + '.json'
        response.headers['session-id'] = sessionID
        try:
            with open(fileName,'w+') as cart:
                data = {}
                data[productName] = 1
                json.dump(data,cart)

                return response
        except:
            return jsonify({"error": "FILE Error"})

#DELETE ITEM FROM CART
@app.route('/cart/remove/<item>',methods = ['DELETE'])
def deleteItem(item):
    response = flask.Response()
    if request.headers.get('session-id'):
        sessionID =  request.headers['session-id']
        fileName =  str(sessionID)+'.json'
        if(path.exists(fileName)):
            cart =  open(fileName,'r')
            data = json.load(cart)
            cart.close()
            if item in data:
                del data[item]
                cart = open(fileName,'w')
                json.dump(data,cart)
                response.headers['session-id'] = sessionID
                return response
            else:
                return jsonify({"error":"No Such item exists in the cart"}),402

        else:  
            return jsonify({"error":"No Such file exists"}),401
    else: 
        return jsonify({"error":"No Session exists"}),400


#DECREASE AN ITEM FROM CART
@app.route('/cart/decrease/<item>',methods = ['DELETE'])
def decreaseItem(item):
    response = flask.Response()
    if request.headers.get('session-id'):
        sessionID =  request.headers['session-id']
        fileName =  str(sessionID)+'.json'
        if(path.exists(fileName)):
            cart =  open(fileName,'r')
            data = json.load(cart)
            cart.close()
            if item in data:
                data[item] = data[item] - 1
                cart = open(fileName,'w')
                json.dump(data,cart)
                response.headers['session-id'] = sessionID
                return response
            else:
                return jsonify({"error":"No Such item exists in the cart"}),402

        else:  
            return jsonify({"error":"No Such file exists"}),401
    else: 
        return jsonify({"error":"No Session exists"}),400
        

#GET THE CART
@app.route('/cart',methods = ['GET'])
def getCart():
    response = flask.Response()
    if request.headers.get('session-id'):
        sessionID =  request.headers['session-id']
        fileName =  str(sessionID)+'.json'
        if(path.exists(fileName)):
            cart =  open(fileName,'r')
            data = json.load(cart)
            return jsonify(data),200
        else:
            return jsonify({"error":"No Such file exists"}),401
    else:
        return jsonify({"error":"No Such Cart Session exists"}),400



if __name__ == '__main__':
    app.run(debug=True)