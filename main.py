# Module 1 - Create a Blockchain

# To be installed 
# itsdangerous==2.0.1; pip install itsdangerous==2.0.1
# Flask == 0.12.2; pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the librariess


import datetime
import hashlib
import json
from flask import Flask, jsonify
# from flask import Flask

# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        block = {   'index':len(self.chain)+1,
                    'timestamp':str(datetime.datetime.now()),
                    'proof':proof,
                    'previous_hash':previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof


    def hash(self, block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            hash_operation = hashlib.sha256(str(block["proof"]**2 - previous_block["proof"]**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False

            previous_block = self.chain[block_index]
            block_index += 1
        # return len(self.chain)
        return True


# Part 2 Mining our Blockchain

# Creating a Web App

app = Flask(__name__)

# Creating a Blockchain

blockchain = Blockchain()










app = Flask(__name__)
# Mining a new block

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message':'Congratulations, you just mined a block!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous hash': block['previous_hash']}
    return json.dumps(response, indent = 2)

    
# Getting the full blockchain





@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return json.dumps(response, indent = 3)


# Checking if the blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        response = {'message': 'All good, the blockchain is valid'}
    else:
        response = {'message': 'Housten we have a problem, the blockchian is not valid'}
    return json.dumps(response, indent=2)



# if __name__ == '__main__':
app.run(debug=True)