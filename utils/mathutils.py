import math


class MathUtils:
  # converts decimal odds to american odds
  @staticmethod
  def decimal_to_american(decimal_odds):
    if decimal_odds >= 2:
      american_odds = round((decimal_odds - 1) * 100)
    else:
      american_odds = round((-1 / (decimal_odds - 1)) * 100)
    return american_odds

  # converts american to decimal odds
  @staticmethod
  def american_to_decimal(american_odds):
    if american_odds >= 0:
      decimal_odds = round((american_odds / 100) + 1, 2)
    else:
      decimal_odds = round((-100 / american_odds) + 1, 2)
    return decimal_odds

  # takes in American odds and wagers on each and calculates the arbitrage by returning a percentage:
  def calculate_arbitrage(odds1, odds2):
    total = 1 / (odds1 / 100) + 1 / (odds2 / 100)
    arb_percentage = round((1 - (1 / total)) * 100, 2)
    return arb_percentage

  # takes in two odds and returns a boolean indicating whether an arb opportunity exists:
  def arb_opportunity_exists(odds1, odds2):
    implied_prob1 = 1 / (odds1 / 100)
    implied_prob2 = 1 / (odds2 / 100)
    return (implied_prob1 + implied_prob2) < 1

  # given no-vig odds and offered odds, return the decimal edge
  def calculate_edge_from_vig(no_vig_odds_1, no_vig_odds_2, team,
                              offered_odds):
    if team == "first":
      no_vig_odds = no_vig_odds_1
    elif team == "second":
      no_vig_odds = no_vig_odds_2
    else:
      raise ValueError("Invalid team specified. Choose 'first' or 'second'.")

    edge = (offered_odds / no_vig_odds) - 1
    return edge

  # takes in two odds and a total amount to wager and tells you the split to place on each:

  def calculate_wager_split(odds, total_wager):
    arb_percentage = calculate_arbitrage(odds[0], odds[1])
    if arb_percentage <= 0:
      raise ValueError("No arbitrage opportunity exists.")
    implied_prob = [1 / (x / 100) for x in odds]
    wager = [
      round((total_wager / sum(implied_prob)) * x, 2) for x in implied_prob
    ]
    return wager

  #calculates the edge
  def calculate_edge(odds, perceived_odds):

    # Find the difference between the perceived and actual odds
    diff = [abs(odds[i] - perceived_odds[i]) for i in range(len(odds))]

    # Calculate perceived edge
    perceived_edge = sum(diff) / sum(odds)

    # Return the perceived edge
    return perceived_edge

  def positive_ev_opportunity_exists(odds, perceived_odds, min=0):
    return calculate_edge(odds, perceived_odds) > min

  def kelly_bet(american_odds, prob, bankroll, kelly_fraction=0.5):
    """
        Calculates the recommended bet size using the Kelly Criterion for American odds.

        Args:
        - american_odds (float): the American odds for the bet
        - prob (float): the perceived probability of the bet winning
        - kelly_fraction (float): the fraction of the optimal bet size to place (usually between 0 and 1)

        Returns:
        - bet_size (float): the recommended bet size
        """
    if american_odds > 0:
      decimal_odds = 1 + (american_odds / 100)
    else:
      decimal_odds = 1 - (100 / american_odds)
    bet_size = (kelly_fraction * ((prob * decimal_odds) -
                                  (1 - prob))) * bankroll
    return round(bet_size, 2)

  def round_down(num, multiple=2.0):
    return (num // multiple) * multiple

  def sameOrBetterOdds(odds):  # where odds = [100, -100]
    if odds[0] == 0:
      return False
    elif odds[1] >= 0:
      return True
    else:
      return 100 / abs(odds[1]) >= odds[0]
