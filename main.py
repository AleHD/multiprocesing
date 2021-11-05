from flask import Flask
import requests
import time
import subprocess


app = Flask(__name__)

lider = None
siguiente = None
me = "uriel"
list_users = ["ale","david","uriel"]
tamaño_criba = 10000

data = {
    "ale":{
        "host":""
    },
    "david":{
        "host":""
    },
    "uriel":{
        "host":""
    },
}

def primesJl():
     subprocess.run(["julia", "temp.jl", f"{tamaño_criba}"])
     return os.popen("ls -l").read()
     

def printPrimes(primes, i):
     primes = primes.split(sep=" ")
     for j in range(i+1, len(primes)+1):
          if(j==1):
              print(j)
     return len(primes)


@app.route("/")
def calculaPrimos():
    global lider
    out = primesJl()    
    i = printPrimes(out)
    lider = data[me]
    t_end = time.time() + 40
    index = 0
    while time.time() < t_end:
        url = data[list_users[index]]["host"]
        response = requests.post(f"{url}/criba", json={
               "i": i
               "mac": gma(),
          }) #como pasamos data?
        print("haciendo calculo")
        index =(index + 1 )%2
     
     # llame julia
     # pasar la lista de primes a los demas
     # recibirla y llamr ajulia



@app.route("/criba", methods=["POST"])
def calculaPorcionCriba(i, pprimes):
     i = request.json["i"]
     pprimes = request.json["pprimes"]
     subprocess.run(["julia", "temp.jl", f"{tamaño_criba}"])
     primes = os.popen(f"julia temp.jl {i} {1000} {pprimes}").read()
     return primes


    
if __name__ == '__main__':
     app.run(host="localhost",debug=True)
     