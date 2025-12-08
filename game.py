import random

class Lot:
    def __init__(self, name, start_price, bid_step):
        self.name = name
        self.start_price = start_price
        self.bid_step = bid_step
        self.current_bid = start_price
        self.leader = None

    def __repr__(self):
        return f"Lot(name={self.name}, start_price={self.start_price}, leader={self.leader}), current_bid={self.current_bid})"
    
    def update_leader(self, name, bid_amount):
        if bid_amount >= self.start_price and self.leader is None:
            self.leader = name
            self.current_bid = bid_amount
            return True
        elif bid_amount >= self.current_bid + self.bid_step:
            self.leader = name
            self.current_bid = bid_amount
            return True
        else:
            print("Bid is lower than starting price or current bid.")
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
    
    def announce_winners(self):
        for lot in self.lots:
            if lot.leader:
                print(f"The winner of the lot '{lot.name}' is {lot.leader} with a bid of {lot.current_bid}.")
                self.get_participant_info(lot.leader).balance -= lot.current_bid
            else:
                print(f"The lot '{lot.name}' had no bids.")
        for p in self.participants:
            print("final capital of participants:")
            print(f"{p.name}: {p.balance:}")
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
            return True
        return False


class Bot(Participant):
    def __init__(self, name, balance, strategy='conservative'):
        super().__init__(name, balance)
        self.strategy = strategy
    
    def make_bid(self, lot):
        if lot.leader == self.name:
            return False
        if self.balance < lot.current_bid + lot.bid_step:
            return False
        
        bid_amount=0
        
        if self.strategy == "aggressive":
            bid_amount= lot.current_bid + lot.bid_step*2
        elif self.strategy == 'conservative':
            bid_amount = lot.current_bid + lot.bid_step
        elif self.strategy == "random":
            bid_amount = lot.current_bid + random.randrange(lot.bid_step, lot.bid_step * 3+1)
        else:
             print(f"({self.name}) Unknown strategy: {self.strategy}.")
             return False
        if bid_amount > self.balance:
            bid_amount = self.balance
        if bid_amount >= lot.current_bid + lot.bid_step:
             return self.place_bid(lot, bid_amount)
        return False
    
def simulate_auction(auction, rounds=10):
    lot1 = Lot("Car", 1000, 100)
    lot2 = Lot("House", 5000, 500)
    lot3 = Lot("Bike", 300, 50)
    lot4 = Lot("picture", 800, 80)
    auction.add_lot(lot1), auction.add_lot(lot2), auction.add_lot(lot3), auction.add_lot(lot4)

    bot1 = Bot("Stive", 10000, strategy='aggressive')
    bot2 = Bot("Alice", 9000, strategy='conservative')
    bot3 = Bot("Bob", 11000, strategy='random')
    auction.add_participant(bot1), auction.add_participant(bot2), auction.add_participant(bot3)

    player_participant = Participant("Platon", 13000)
    auction.add_participant(player_participant)

    for _ in range(rounds):
        for lot in auction.lots:
            for p in auction.participants:
                if isinstance(p, Bot):
                    p.make_bid(lot)

    def get_user_bid():
        try:
            your_choice_lot = input("Enter the lot you want to bid on (Car, House, Bike, picture: ")
            your_bid = int(input("Enter your bid: "))
            p = player_participant.place_bid(your_choice_lot, your_bid)
            return p
        except ValueError:
            print("Invalid input. Please enter a valid lot name and bid amount.")
            return get_user_bid()
    get_user_bid()
    auction.announce_winners()

if __name__ == "__main__":
    auction = Auction()
    simulate_auction(auction, rounds=10)
    
