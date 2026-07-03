from utils import hash_log, get_contract, get_web3
from config import WALLET_ADDRESS, PRIVATE_KEY
from web3 import Web3
from datetime import datetime

w3 = get_web3()
contract = get_contract()

def hash_log(log):
    log = log.strip().replace('\r', '').replace('\n', '')
    return Web3.keccak(text=log).hex()

def generate_log():
    ip = input("Enter IP Address: ")
    attack = input("Enter Attack Type: ")
    severity = input("Enter Severity (Low/Medium/High): ")

    log = f"IP: {ip} | Attack: {attack} | Severity: {severity}"
    return log

def store_log(log):
    log_hash = hash_log(log)

    print("Generated Log:", log)
    print("Log Hash (keccak):", log_hash)

    nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)

    tx = contract.functions.storeLog(log).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.to_wei('10', 'gwei')
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print("Transaction Sent! Hash:", w3.to_hex(tx_hash))

def verify_log(original_log, log_id):

    original_log = original_log.strip().replace('\r', '').replace('\n', '')

    log_bytes = original_log.encode('utf-8')
    
    new_hash = Web3.keccak(log_bytes).hex()

    stored_log = contract.functions.logs(log_id).call()
    stored_hash = contract.functions.getLogHash(log_id).call().hex()

    print(f"\n✅ Verifying Log ID {log_id}...")
    print(f"Input Log: '{original_log}'")
    print(f"Stored Log: '{stored_log}'")
    print(f"Generated Hash (SHA-256): '{new_hash}'")
    print(f"Stored Hash: '{stored_hash}'")

    if isinstance(stored_hash, bytes):
        stored_hash = stored_hash.hex()

    if new_hash == stored_hash:
        print("✅ Log is AUTHENTIC (Not Tampered)")
    else:
        print("❌ Log is TAMPERED")

        with open("alerts.txt", "a") as f:
            f.write(f"[{datetime.now()}] TAMPERING DETECTED: {original_log}\n")

def view_logs():
    logs = contract.functions.getLogs().call()

    print("\nStored Logs in Blockchain:")
    for i, log in enumerate(logs):
        print(f"{i+1}. {log}")

def main():
    print("Connected:", w3.is_connected())

    print("\n1. Store Logs")
    print("2. Verify Log")

    choice = input("Enter choice: ")

    if choice == "1":
        n = int(input("How many logs do you want to enter? "))
        for i in range(n):
            print(f"\nEnter details for Log {i+1}")
            log = generate_log()
            store_log(log)
        print("\nFetching logs from blockchain...")
        view_logs()

    elif choice == "2":
        log_id = int(input("Enter log ID to verify (e.g., 0, 1, 2): "))
        print("Enter the log content to verify: ")
        original_log = generate_log()
        verify_log(original_log, log_id)        

if __name__ == "__main__":
    main()