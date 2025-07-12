import tkinter as tk
from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service

# Create a wallet (or open existing)
WALLET_NAME = 'WALL-let'
wallet = Wallet.create(WALLET_NAME) if not Wallet.exists(WALLET_NAME) else Wallet(WALLET_NAME)

# Use testnet for safety
wallet.network = 'testnet'

# GUI setup
root = tk.Tk()
root.title("Bitcoin Wallet (Testnet)")
root.geometry("400x300")

def update_balance():
    wallet.utxos_update()
    balance = wallet.balance()
    balance_label.config(text=f"Balance: {balance} BTC")

def show_address():
    key = wallet.get_key()
    address_label.config(text=f"Receive Address:\n{key.address}")

def send_btc():
    to = send_to_entry.get()
    amount = float(send_amount_entry.get())
    try:
        tx = wallet.send_to(to, amount)
        result_label.config(text=f"Sent {amount} BTC\nTX ID: {tx.txid}")
        update_balance()
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Labels & Buttons
balance_label = tk.Label(root, text="Balance: ---", font=("Arial", 14))
balance_label.pack(pady=10)

address_label = tk.Label(root, text="Receive Address: ---", wraplength=380)
address_label.pack()

tk.Button(root, text="Show My Address", command=show_address).pack(pady=5)
tk.Button(root, text="Update Balance", command=update_balance).pack(pady=5)

# Send BTC Section
tk.Label(root, text="Send BTC to:").pack()
send_to_entry = tk.Entry(root, width=40)
send_to_entry.pack()

tk.Label(root, text="Amount (BTC):").pack()
send_amount_entry = tk.Entry(root, width=20)
send_amount_entry.pack()

tk.Button(root, text="Send", command=send_btc).pack(pady=10)

result_label = tk.Label(root, text="", wraplength=380)
result_label.pack()

# Start
update_balance()
root.mainloop()
