import re

from flask import Flask, request, render_template, url_for, redirect, flash, session
from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract_address, abi=abi)
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'login' in request.form:
        return redirect(url_for('tologin'))
    if request.method == 'POST':
        public_key = request.form.get('publickey')
        password = request.form.get('password')
        if public_key and password !='':
            try:
                w3.geth.personal.unlock_account(public_key, password)
                return redirect(url_for('main', public_key=public_key))
            except ValueError:
                error = "Invalid public key or password"
                return render_template("wronglogpass.html", error=error)
        else:
            return render_template("emptylogpass.html")
    else:
        return render_template("login.html")


@app.route('/yourpublickey')
def yourpublickey():
    account = request.args.get('account')
    return render_template("yourpublickey.html", account=account)



@app.route('/main/<public_key>', methods=['GET', 'POST'])
def main(public_key):
    if request.method == 'POST':
        try:
            if 'id_estate' in request.form:
                id_estate = int(request.form.get('id_estate')) - 1
                status = bool(int(request.form.get('status')))
                tx_hash = contract.functions.updateEstateStatus(id_estate, status).transact({
                    "from": public_key,
                })
                balance = w3.eth.get_balance(public_key)
                balance_smart = contract.functions.getBalance().call({
                    "from": public_key,
                })
                estates = contract.functions.getEstates().call({
                    "from": public_key,
                })
                adds = contract.functions.getAds().call({
                    "from": public_key,
                })
                return render_template("main.html", public_key=public_key, balance=balance, balance_smart=balance_smart,
                                       estates=estates, adds=adds)
            elif 'id_ad' in request.form:
                id_ad = int(request.form.get('id_ad')) - 1
                status = int(request.form.get('status'))
                tx_hash = contract.functions.updateAdStatus(id_ad, status).transact({
                    "from": public_key,
                })
                balance = w3.eth.get_balance(public_key)
                balance_smart = contract.functions.getBalance().call({
                    "from": public_key,
                })
                estates = contract.functions.getEstates().call({
                    "from": public_key,
                })
                adds = contract.functions.getAds().call({
                    "from": public_key,
                })
                return render_template("main.html", public_key=public_key, balance=balance, balance_smart=balance_smart,
                                       estates=estates, adds=adds)

            elif 'submit_create_estate' in request.form:
                size = int(request.form['size'])
                estate_address = str(request.form['estate_address'])
                estate_type = int(request.form['estate_type'])
                tx_hash = contract.functions.createEstate(size, estate_address, estate_type).transact({
                    "from": public_key,
                })
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash.hex())
                if receipt.status == 1:
                    flash("estate created", 'success')
                    balance = w3.eth.get_balance(public_key)
                    balance_smart = contract.functions.getBalance().call({
                        "from": public_key,
                    })
                    estates = contract.functions.getEstates().call({
                        "from": public_key,
                    })
                    adds = contract.functions.getAds().call({
                        "from": public_key,
                    })
                    return render_template("main.html", public_key=public_key, balance=balance, balance_smart=balance_smart,
                                           estates=estates, adds=adds)
                else:
                    balance = w3.eth.get_balance(public_key)
                    balance_smart = contract.functions.getBalance().call({
                        "from": public_key,
                    })
                    estates = contract.functions.getEstates().call({
                        "from": public_key,
                    })
                    adds = contract.functions.getAds().call({
                        "from": public_key,
                    })
                    return render_template("main.html", public_key=public_key, balance=balance,
                                           balance_smart=balance_smart,
                                           estates=estates, adds=adds)
            elif 'submit_create_ad' in request.form:
                id_estate = int(request.form['id_estate'])
                price = int(request.form['price'])
                tx_hash = contract.functions.createAd(id_estate, price).transact({
                    "from": public_key,
                })
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash.hex())
                if receipt.status == 1:
                    id_estate = int(request.form['id_estate'])
                    price = int(request.form['price'])
                    tx_hash = contract.functions.createAd(id_estate, price).transact({
                        "from": public_key,
                    })
                    status = False
                    contract.functions.updateEstateStatus(id_estate, status).transact({
                        'from': public_key
                    })
                    balance = w3.eth.get_balance(public_key)
                    balance_smart = contract.functions.getBalance().call({
                        "from": public_key,
                    })
                    estates = contract.functions.getEstates().call({
                        "from": public_key,
                    })
                    adds = contract.functions.getAds().call({
                        "from": public_key,
                    })
                    return render_template("main.html", public_key=public_key, balance=balance,
                                           balance_smart=balance_smart,
                                           estates=estates, adds=adds)
                else:
                    balance = w3.eth.get_balance(public_key)
                    balance_smart = contract.functions.getBalance().call({
                        "from": public_key,
                    })
                    estates = contract.functions.getEstates().call({
                        "from": public_key,
                    })
                    adds = contract.functions.getAds().call({
                        "from": public_key,
                    })
                    return render_template("main.html", public_key=public_key, balance=balance,
                                           balance_smart=balance_smart,
                                           estates=estates, adds=adds)
            elif 'send' in request.form:
                amount = int(request.form['amount'])
                tx_hash = contract.functions.withdraw(amount).transact({
                    'from': public_key,
                })
                balance = w3.eth.get_balance(public_key)
                balance_smart = contract.functions.getBalance().call({
                    "from": public_key,
                })
                estates = contract.functions.getEstates().call({
                    "from": public_key,
                })
                adds = contract.functions.getAds().call({
                    "from": public_key,
                })
                return render_template("main.html", public_key=public_key, balance=balance,
                                       balance_smart=balance_smart,
                                       estates=estates, adds=adds)
            elif 'submit_buy_ad' in request.form:
                id_ad = int(request.form['id_ad'])
                tx_hash = contract.functions.buyEstate(id_ad).transact({
                    'from': public_key,
                    'value': 0
                })
                status = False
                tx_hash = contract.functions.updateAdStatus(id_ad, status).transact({
                    "from": public_key,
                })
                balance = w3.eth.get_balance(public_key)
                balance_smart = contract.functions.getBalance().call({
                    "from": public_key,
                })
                estates = contract.functions.getEstates().call({
                    "from": public_key,
                })
                adds = contract.functions.getAds().call({
                    "from": public_key,
                })
                return render_template("main.html", public_key=public_key, balance=balance, balance_smart=balance_smart,
                                       estates=estates, adds=adds)



        except Exception as e:
            return redirect(url_for('main', public_key=public_key))
    try:
        balance = w3.eth.get_balance(public_key)
        balance_smart = contract.functions.getBalance().call({
            "from": public_key,
        })
        estates = contract.functions.getEstates().call({
            "from": public_key,
        })
        adds = contract.functions.getAds().call({
            "from": public_key,
        })
        return render_template("main.html", public_key=public_key, balance=balance, balance_smart=balance_smart, estates=estates, adds=adds)
    except Exception:
        return "Error"



@app.route('/tologin', methods=['POST', 'GET'])
def tologin():
    if request.method == 'POST':
        new_password = request.form.get('newpass')
        if new_password:
            try:
                account = w3.geth.personal.new_account(new_password)
                return render_template("yourpublickey.html", account=account)
            except ValueError:
                flash("Invalid password", 'danger')
                return redirect(url_for('tologin'))
        else:
            flash("Password cannot be empty", 'danger')
            return redirect(url_for('tologin'))
    else:
        return render_template("tologin.html")


def ToPay(account, value):
    try:
        tx_hash = contract.functions.toPay().transact({
            'from': account,
            'value': value,
        })
    except Exception as ex:
        pass


def get_balance(account):
    balance = contract.functions.getBalance().call({
        "from": account,
    })
    return balance

def withdraw(account, amount):
    try:
        tx_hash = contract.functions.withdraw(amount).transact({
            'from': account,
        })
    except Exception as ex:
        pass


def create_estate(account, size, estateAdres, typeEs):
    tx_hash = contract.functions.createEstate(size, estateAdres, typeEs).transact({
        'from': account,
    })


def get_estates(account):
    estates = contract.functions.getEstates().call({
        "from": account,
    })
    return estates


def get_ads(account):
    ads = contract.functions.getAds().call({
        "from": account,
    })
    return ads


def buy_estate(account, num_ad):
    try:
        tx_hash = contract.functions.buyEstate(num_ad).transact({
            'from': account,
        })
    except:
        pass



def check_password(password):
    # Минимальная длина пароля
    if len(password) < 12:
        flash("Password must be at least 12 characters long", 'danger')
        return False

    # Отсутствие пробелов
    if " " in password:
        flash("Password cannot contain spaces", 'danger')
        return False

    # Наличие хотя бы одной заглавной и строчной буквы
    if not re.search("[a-z]", password) or not re.search("[A-Z]", password):
        flash("Password must contain at least one lowercase and one uppercase letter", 'danger')
        return False

    # Наличие хотя бы одной цифры
    if not re.search("[0-9]", password):
        flash("Password must contain at least one digit", 'danger')
        return False

    # Наличие хотя бы одного специального символа
    if not re.search("(!@#$%^&*)", password):
        flash("Password must contain at least one special character (!@#$%^&*)", 'danger')
        return False

    if re.search("^(.*)(password|1234)(.*)$", password):
        flash("Password cannot be a simple pattern (e.g., password123)", 'danger')
        return False

    return True

@app.errorhandler(500)
def errorHandle(error):
    return render_template("500.html"), 500

@app.errorhandler(404)
def errorHandle(error):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=False)