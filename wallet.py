import tkinter as tk
from tkinter import simpledialog, messagebox
from bitcoinlib.wallets import Wallet, WalletError
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.keys import HDKey

APP_TITLE = "Testnet Bitcoin Wallet"
NETWORK = "testnet"
wallet = None  # Global wallet reference


# ========== LOGIN SCREEN ==========
def login_screen():
    login = tk.Tk()
    login.title(APP_TITLE)
    login.geometry("350x250")

    def create_wallet():
        name = simpledialog.askstring("Create Wallet", "Wallet Name:")
        if not name:
            return

        try:
            global wallet
            m = Mnemonic()
            mnemonic = m.generate()
            key = HDKey().from_passphrase(mnemonic, network=NETWORK)

            wallet = Wallet.create(name, keys=key, network=NETWORK)
            messagebox.showinfo("Wallet Created", f"Save this mnemonic phrase securely:\n\n{mnemonic}")
            login.destroy()
            main_wallet_ui()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_wallet():
        name = simpledialog.askstring("Load Wallet", "Enter Wallet Name (on disk):")
        if not name:
            return

        try:
            global wallet
            wallet = Wallet(name)
            wallet.network = NETWORK
            login.destroy()
            main_wallet_ui()
        except WalletError:
            messagebox.showerror("Not Found", "Wallet not found on this computer.")

    def import_wallet():
        mnemonic = simpledialog.askstring("Import Wallet", "Enter 12/24-word mnemonic phrase:")
        if not mnemonic:
            return

        name = simpledialog.askstring("Wallet Name", "Choose a name to save this wallet as:")
        if not name:
            return

        try:
            global wallet
            wallet = Wallet.create(name, keys=mnemonic, network=NETWORK)
            messagebox.showinfo("Success", f"Wallet imported and saved as '{name}'")
            login.destroy()
            main_wallet_ui()
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

    tk.Label(login, text=APP_TITLE, font=("Arial", 14)).pack(pady=10)
    tk.Button(login, text="Create New Wallet", command=create_wallet, width=25).pack(pady=5)
    tk.Button(login, text="Load Existing Wallet (on PC)", command=load_wallet, width=25).pack(pady=5)
    tk.Button(login, text="Import from Mnemonic", command=import_wallet, width=25).pack(pady=5)

    login.mainloop()


# ========== MAIN WALLET UI ==========
def main_wallet_ui():
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("420x450")

    def update_balance():
        try:
            wallet.utxos_update()
            balance = wallet.balance()
            balance_label.config(text=f"Balance: {balance} BTC")
        except Exception as e:
            balance_label.config(text="Balance: Error")

    def show_address():
        key = wallet.get_key(0)
        address_label.config(text=f"Address:\n{key.address}")

    def send_btc():
        to = send_to_entry.get()
        try:
            amount = float(send_amount_entry.get())
        except ValueError:
            result_label.config(text="Error: Invalid BTC amount")
            return

        try:
            tx = wallet.send_to(to, amount)
            result_label.config(text=f"Sent {amount} BTC\nTX ID: {tx.txid}")
            update_balance()
        except Exception as e:
            result_label.config(text=f"Error: {e}")

    def show_keys():
        try:
            key = wallet.get_key(0)
            public_key = key.key_public.hex()
            messagebox.showinfo("Key Info", f"Address: {key.address}\n\n"
                                            f"Public Key:\n{public_key}\n\n"
                                            f"Private Key (WIF):\n{key.wif}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve keys:\n{e}")

    def logout():
        root.destroy()
        login_screen()

    tk.Label(root, text=APP_TITLE, font=("Arial", 14)).pack(pady=10)

    balance_label = tk.Label(root, text="Balance: ---", font=("Arial", 12))
    balance_label.pack(pady=5)

    address_label = tk.Label(root, text="Address: ---", wraplength=400)
    address_label.pack()

    tk.Button(root, text="Show My Address", command=show_address).pack(pady=4)
    tk.Button(root, text="Show Public/Private Keys", command=show_keys).pack(pady=4)
    tk.Button(root, text="Update Balance", command=update_balance).pack(pady=4)

    tk.Label(root, text="Send BTC to:").pack()
    send_to_entry = tk.Entry(root, width=45)
    send_to_entry.pack()

    tk.Label(root, text="Amount (BTC):").pack()
    send_amount_entry = tk.Entry(root, width=20)
    send_amount_entry.pack()

    tk.Button(root, text="Send", command=send_btc).pack(pady=8)

    result_label = tk.Label(root, text="", wraplength=380)
    result_label.pack(pady=5)

    tk.Button(root, text="Logout / Return to Main Menu", command=logout, fg="red").pack(pady=10)

    update_balance()
    root.mainloop()


# ========== START APP ==========
login_screen()
