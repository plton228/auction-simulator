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