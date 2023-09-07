import pytest
from decimal import Decimal
from market_classes import Asset, AssetPrice, Transaction, Portfolio, MarketSimulator

# Fixtures for common objects
@pytest.fixture
def asset_lkoh():
    return Asset("LKOH")

@pytest.fixture
def asset_sber():
    return Asset("SBER")

# Asset Class Tests
@pytest.mark.asset
@pytest.mark.parametrize("asset_name, asset_value", [("LKOH", AssetPrice["LKOH"].value)])
def test_asset_initialization(asset_name, asset_value):
    asset = Asset(asset_name)
    assert asset.name == asset_name
    assert asset.price == asset_value

@pytest.mark.asset
@pytest.mark.parametrize("new_price", [Decimal(6000), Decimal(7000)])
def test_asset_price_update(asset_lkoh, new_price):
    asset_lkoh.update_price(new_price)
    assert asset_lkoh.price == new_price
    assert asset_lkoh.price_history[-1] == new_price

# Transaction Class Tests
@pytest.mark.transaction
@pytest.mark.parametrize("quantity", [1, 2, 3])
def test_transaction(asset_sber, quantity):
    transaction = Transaction(asset_sber, quantity)
    assert transaction.asset == asset_sber
    assert transaction.quantity == quantity

# Portfolio Class Tests
@pytest.mark.portfolio
def test_portfolio(asset_lkoh, asset_sber):
    portfolio = Portfolio()
    transaction1 = Transaction(asset_lkoh, 1)
    transaction2 = Transaction(asset_sber, 2)
    portfolio.buy(transaction1)
    portfolio.buy(transaction2)
    assert portfolio.assets['LKOH'] == AssetPrice.LKOH.value
    assert portfolio.assets['SBER'] == AssetPrice.SBER.value * 2

# MarketSimulator Class Tests
@pytest.mark.simulator
def test_market_simulator(asset_lkoh, asset_sber):
    simulator = MarketSimulator()
    transaction1 = Transaction(asset_lkoh, 1)
    transaction2 = Transaction(asset_sber, 2)
    simulator.execute_transactions([transaction1, transaction2])
    assert simulator.get_portfolio_value() == AssetPrice.LKOH.value + (AssetPrice.SBER.value * 2)
