import tkinter as tk
from tkinter import simpledialog, messagebox
from bitcoinlib.wallets import Wallet, WalletError
from bitcoinlib.mnemonic import Mnemonic

APP_TITLE = "Testnet Bitcoin Wallet"
NETWORK = "testnet"  # Use string, NOT Network object
wallet = None  # Global wallet reference


# ========== LOGIN SCREEN ==========
def login_screen():
    def create_wallet():
        global wallet
        wallet_name = simpledialog.askstring("Create Wallet", "Enter a wallet name:")
        if wallet_name:
            try:
                mnemonic = Mnemonic().generate()
                wallet = Wallet.create(wallet_name, keys=mnemonic, network=NETWORK)
                messagebox.showinfo("Wallet Created", f"Wallet '{wallet_name}' created!\n\nMnemonic:\n{mnemonic}")
                login.destroy()
                main_wallet_ui()
            except WalletError as e:
                messagebox.showerror("Error", str(e))

    def import_wallet():
        global wallet
        wallet_name = simpledialog.askstring("Import Wallet", "Enter a wallet name:")
        mnemonic = simpledialog.askstring("Import Wallet", "Enter your 12/24-word mnemonic:")
        if wallet_name and mnemonic:
            try:
                wallet = Wallet.create(wallet_name, keys=mnemonic, network=NETWORK)
                messagebox.showinfo("Wallet Imported", f"Wallet '{wallet_name}' imported successfully!")
                login.destroy()
                main_wallet_ui()
            except WalletError as e:
                messagebox.showerror("Error", str(e))

    login = tk.Tk()
    login.title(APP_TITLE)
    login.geometry("350x250")

    tk.Label(login, text="Welcome to Testnet Bitcoin Wallet!", font=("Arial", 12)).pack(pady=20)
    tk.Button(login, text="Create Wallet", width=25, command=create_wallet).pack(pady=10)
    tk.Button(login, text="Import Wallet", width=25, command=import_wallet).pack(pady=10)
    tk.Button(login, text="Exit", width=25, command=login.destroy).pack(pady=10)

    login.mainloop()


# ========== MAIN WALLET UI ==========
def main_wallet_ui():
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("400x350")

    balance_label = tk.Label(root, text="Balance: Loading...", font=("Arial", 12))
    balance_label.pack(pady=10)

    def update_balance():
        try:
            wallet.utxos_update()
            balance = wallet.balance()
            balance_label.config(text=f"Balance: {balance} BTC")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_address():
        try:
            key = wallet.get_key()
            messagebox.showinfo("Wallet Address", f"Address:\n{key.address}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_keys():
        try:
            key = wallet.get_key()
            priv = key.wif
            pub = key.key().public_hex
            messagebox.showinfo("Keys", f"Private Key:\n{priv}\n\nPublic Key:\n{pub}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def send_btc():
        to_address = simpledialog.askstring("Send BTC", "Enter destination address:")
        amount = simpledialog.askfloat("Send BTC", "Enter amount in BTC:")
        if to_address and amount:
            try:
                tx = wallet.send_to(to_address, amount, network=NETWORK)
                messagebox.showinfo("Transaction Sent", f"TXID:\n{tx.txid}")
                update_balance()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    tk.Button(root, text="Update Balance", width=25, command=update_balance).pack(pady=10)
    tk.Button(root, text="Show Address", width=25, command=show_address).pack(pady=10)
    tk.Button(root, text="Show Keys", width=25, command=show_keys).pack(pady=10)
    tk.Button(root, text="Send BTC", width=25, command=send_btc).pack(pady=10)
    tk.Button(root, text="Exit", width=25, command=root.destroy).pack(pady=10)

    update_balance()
    root.mainloop()


# ========== RUN ==========
if __name__ == "__main__":
    login_screen()
