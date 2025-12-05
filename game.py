import random

class Lot:
    def __init__(self, name, start_price, bid_step, leader=None, current_bid=0):
        self.name = name
        self.start_price = start_price
        self.bid_step = bid_step

    def __repr__(self):
        return f"Lot(name={self.name}, start_price={self.start_price}, leader={self.leader}), current_bid={self.current_bid})"
    
    def update_leader(self, name, bin):
        if bin >= self.start_price and bin >= self.current_bid + self.bid_step:
            self.leader = name
            self.current_bid = bin
            return True
        else:
            print("Bid is lower than starting price.")
            return False
        

class Auction:
    def __init__(self):
        self.lots = []
        self.participants = []

    def add_lot(self, lot):
        self.lots.append(lot)

    def add_participant(self, participant):
        self.participants.append(participant)

    def get_lot_info(self, lot_name):
        for lot in self.lots:
            if lot.name == lot_name:
                return lot
        return None

    def get_participant_info(self, participant_name):
        for participant in self.participants:
            if participant.name == participant_name:
                return participant
        return None
    

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


class bot(Participant):
    def __init__(self, name, balance, strategy='conservative'):
        super().__init__(name, balance)
        self.strategy = strategy
    
    def make_bid(self, lot):
        if lot.leader == self.name:
            return False
        if self.balance < lot.current + lot.bid_step:
            return False
        
        bit_amount=0
        
        if self.strategy == "aggressive":
            aggrissive_step = lot.bid_step*2
            bit_amount= lot.current_bid + aggrissive_step
        if self.strategy == 'conservative':
            bit_amount = lot.current_bid + lot.bid_step
        if self.strategy == "random":
            max_step = lot.bid_step * 4
            random_bid = lot.current_bid + random.randrange(lot.bid_step, max_step+1)
