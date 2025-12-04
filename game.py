class Lot:
    def __init__(self, name, start_price, leader):
        self.name = name
        self.start_price = start_price
        self.leader = None

    def __repr__(self):
        return f"Lot(name={self.name}, start_price={self.start_price}, leader={self.leader})"
    
    def update_leader(self, name, bin):
        if bin >= self.start_price:
            self.leader = name
            return True
        else:
            print("Bid is lower than starting price.")
            return False

class Participant:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def __repr__(self):
        return f"Participant(name={self.name}, balance={self.balance})"
    
    def place_bid(self, lot, bid_amount):
        if bid_amount > self.balance:
            print("Insufficient balance to place the bid.")
            return False
        if lot.update_leader(self.name, bid_amount):
            self.balance -= bid_amount
            return True
        return False