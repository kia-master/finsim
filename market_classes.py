from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Type, List, Dict
from random import uniform


class AssetPrice(Enum):
    """Enum class to represent the price of different assets."""
    LKOH = Decimal(5896)
    SBER = Decimal(250)


class Asset:
    """Class to represent an asset in the market.
    
    Attributes:
        name (str): The name of the asset, should match an entry in AssetPrice.
        price (Decimal): The current price of the asset.
        price_history (List[Decimal]): The history of price changes.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.price: Decimal = AssetPrice[name].value
        self.price_history: List[Decimal] = [self.price]

    def update_price(self, new_price: Decimal) -> None:
        """Updates the price of the asset and stores it in the history."""
        self.price = new_price.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        self.price_history.append(self.price)

    def simulate_price_change(self, volatility: Decimal = Decimal("0.05")) -> None:
        """Simulate a price change based on a volatility factor.
        
        Args:
            volatility (Decimal): The volatility factor, default is 0.05.
        """
        percentage_change = uniform(float(-volatility), float(volatility))
        new_price = self.price * Decimal(1 + percentage_change)
        self.update_price(new_price)


class Transaction:
    """Class to represent a transaction in the market."""

    def __init__(self, asset: Type[Asset], quantity: int) -> None:
        self.asset: Type[Asset] = asset
        self.quantity: int = quantity


class Portfolio:
    """Class to manage a portfolio of assets."""

    def __init__(self) -> None:
        self.assets: Dict[str, Decimal] = defaultdict(Decimal)

    def buy(self, transaction: Type[Transaction]) -> None:
        asset_name: str = transaction.asset.name
        self.assets[asset_name] += transaction.quantity * transaction.asset.price

    def sell(self, transaction: Type[Transaction]) -> None:
        asset_name: str = transaction.asset.name
        self.assets[asset_name] -= transaction.quantity * transaction.asset.price

    def get_value(self) -> Decimal:
        return sum(price for price in self.assets.values())


class MarketSimulator:
    """Class to simulate market operations."""

    def __init__(self) -> None:
        self.portfolio: Type[Portfolio] = Portfolio()

    def execute_transactions(self, transactions: List[Type[Transaction]]) -> None:
        for transaction in transactions:
            if transaction.quantity > 0:
                self.portfolio.buy(transaction)
            else:
                self.portfolio.sell(transaction)

    def get_portfolio_value(self) -> Decimal:
        return self.portfolio.get_value()
