import random

class Lot:
    def __init__(self, name, start_price, bid_step):
        self.name = name
        self.start_price = start_price
        self.bid_step = bid_step
        self.current_bid = start_price
        self.leader = None

    def __repr__(self):
        return f"Lot(name={self.name}, start_price={self.start_price}, leader={self.leader}, current_bid={self.current_bid})"
    
    def update_leader(self, name, bid_amount):
        if self.leader is None:
            if bid_amount >= self.start_price:
                self.leader = name
                self.current_bid = bid_amount
                print(f"[{self.name}] New leader: {name} with bid: {bid_amount}")
                return True
            else:
                print("Bid is lower than starting price.")
                return False
        elif bid_amount >= self.current_bid + self.bid_step:
            self.leader = name
            self.current_bid = bid_amount
            print(f"[{self.name}] New leader: {name} with bid: {bid_amount}")
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
        print("\nAuction Results:")
        for lot in self.lots:
            if lot.leader:
                print(f"The winner of the lot '{lot.name}' is {lot.leader} with a bid of {lot.current_bid}.")
                winner = self.get_participant_info(lot.leader)
                if winner:
                    winner.balance -= lot.current_bid
            else:
                print(f"The lot '{lot.name}' had no bids.")
        print("\nFinal capital of participants:")
        for p in self.participants:
            print(f"{p.name}: {p.balance}")

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
        self.decision_pool = (True, False)
    
    def make_bid(self, lot):
        if not random.choice(self.decision_pool):
            return False    
        if lot.leader == self.name:
            return False
        if self.balance < lot.current_bid + lot.bid_step:
            return False
        
        bid_amount = 0
        
        if self.strategy == "aggressive":
            bid_amount = lot.current_bid + lot.bid_step * 3
        elif self.strategy == 'conservative':
            bid_amount = lot.current_bid + lot.bid_step
        elif self.strategy == "random":
            bid_amount = lot.current_bid + random.randrange(lot.bid_step, lot.bid_step * 3 + 1)
        else:
             print(f"({self.name}) Unknown strategy: {self.strategy}.")
             return False
        
        if bid_amount > self.balance:
            bid_amount = self.balance
            
        return self.place_bid(lot, bid_amount)
    
def simulate_auction(auction, rounds=10):
    lot1 = Lot("Car", 1000, 100)
    lot2 = Lot("House", 4000, 500)
    lot3 = Lot("Bike", 500, 50)
    lot4 = Lot("Picture", 800, 80)
    auction.add_lot(lot1)
    auction.add_lot(lot2)
    auction.add_lot(lot3)
    auction.add_lot(lot4)

    bot1 = Bot("Stive", 10000, strategy='aggressive')
    bot2 = Bot("Alice", 9000, strategy='conservative')
    bot3 = Bot("Bob", 11000, strategy='random')
    auction.add_participant(bot1)
    auction.add_participant(bot2)
    auction.add_participant(bot3)

    player_participant = Participant("Platon", 13000)
    auction.add_participant(player_participant)

    def get_user_bid():
            try:
                print(f"\nAvailable lots: {[f'{l.name}: {l.current_bid}' for l in auction.lots]}")
                user_input_lot = input(f"Enter the lot you want to bid on (or 'skip'): ")
                if user_input_lot.lower() == 'skip':
                    return False

                lot_object = auction.get_lot_info(user_input_lot)

                if lot_object is None:
                    print("Lot not found. Please enter a valid lot name.")
                    return get_user_bid()
                
                if lot_object.leader is None:
                    min_bid = lot_object.start_price
                else:
                    min_bid = lot_object.current_bid + lot_object.bid_step

                your_bid = int(input(f"Current bid for {lot_object.name} is {lot_object.current_bid}. Min bid required: {min_bid}. Enter your bid: "))
                
                if your_bid > player_participant.balance:
                    print("You do not have enough balance for this bid.")
                    return get_user_bid()
                
                if your_bid < min_bid:
                    print(f"Your bid is too low. It must be at least {min_bid}.")
                    return get_user_bid()
                
                player_participant.place_bid(lot_object, your_bid)
                return True
                
            except ValueError:
                print("Invalid input. Please enter a number for the bid.")
                return get_user_bid()
        
    for i in range(rounds):
        print(f"\n Round {i+1}")
        for p in auction.participants:
            if isinstance(p, Bot):
                available_lots = [l for l in auction.lots if l.leader != p.name]
                if available_lots:
                    lot = random.choice(available_lots)
                    p.make_bid(lot)
        get_user_bid()

    auction.announce_winners()

if __name__ == "__main__":
    auction = Auction()
    simulate_auction(auction, rounds=10)