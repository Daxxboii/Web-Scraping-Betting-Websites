import datetime
from markets import Markets
from sportsbooks import Sportsbooks

# represents a scraped bet that may either be arbitrage or positive ev
class ScrapedBet:
    stake = 10
    def __init__(self, perceievedDecimalEdges, date, sport, market, team, opponent, odds, sportsbook, implied_probs):
        self.perceievedDecimalEdges = perceievedDecimalEdges # this would be ROI for arbitrage
        self.date = date
        self.sport = sport
        self.market = market
        self.team = team
        self.opponent = opponent
        self.odds = odds
        self.sportsbook = sportsbook
        self.implied_probs = implied_probs # no vig odds

    def __eq__(self, other):
        if not isinstance(other, ScrapedBet):
            return False
        return (
            self.date == other.date
            and self.sport == other.sport
            and self.market == other.market
            and self.team == other.team
            and self.opponent == other.opponent
            and self.odds == other.odds
            and self.sportsbook == other.sportsbook
            and self.perceievedDecimalEdges == other.perceievedDecimalEdges
        )  

    def expected_value(self):
        return sum([self.stake * self.odds[i] * self.implied_probs[i] - self.stake for i in range(len(self.odds))])

    def __str__(self):
        return f"{self.date} - {self.sport} - {self.market} - {self.team} vs {self.opponent} - {self.sportsbook} - {self.odds} - {self.implied_probs} - EV: {self.expected_value():.2f}"

#web-scrapped positie ev bet
scraped_bet = ScrapedBet([0.05, 0.06, 0.07], "2023-03-15", "Basketball", Markets.FIRST_HALF_SECOND_HALF, "Virginia Tech", "Cincinati", "Cincinati", [-110, -120, -100], [Sportsbooks.FAN_DUEL, Sportsbooks.DRAFT_KINGS, Sportsbooks.CAESAR_SPORTSBOOK])
#Webscrapped single positive ev bet