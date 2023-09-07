from decimal import Decimal
from market_classes import MarketSimulator, Asset, Transaction
import random


def run_market_simulation():
    try:
        print("Starting Market Simulation...")

        simulator: MarketSimulator = MarketSimulator()
        print("Market Simulator initialized.")

        lkoh: Asset = Asset("LKOH")
        sber: Asset = Asset("SBER")
        print(f"Assets initialized. LKOH: {lkoh.price}, SBER: {sber.price}")

        prev_lkoh_price: Decimal = lkoh.price
        prev_sber_price: Decimal = sber.price

        # Simulate multiple rounds
        for i in range(1, 11):
            print(f"\n--- Round {i} ---")

            # Simulate price change
            lkoh.simulate_price_change()
            sber.simulate_price_change()
            print(f"Prices after simulation. LKOH: {lkoh.price}, SBER: {sber.price}")

            # Decide whether to buy or sell based on price change and random choice
            lkoh_action: int = 1 if lkoh.price > prev_lkoh_price and random.choice([True, False]) else -1
            sber_action: int = 2 if sber.price > prev_sber_price and random.choice([True, False]) else -2

            # Initialize Transactions
            transaction1: Transaction = Transaction(lkoh, lkoh_action)
            transaction2: Transaction = Transaction(sber, sber_action)

            # Execute Transactions
            simulator.execute_transactions([transaction1, transaction2])
            lkoh_transaction_type = "Bought" if lkoh_action > 0 else "Sold"
            sber_transaction_type = "Bought" if sber_action > 0 else "Sold"
            print(f"Executed transactions. {lkoh_transaction_type} {abs(lkoh_action)} of LKOH and {sber_transaction_type} {abs(sber_action)} of SBER.")

            # Get Portfolio Value
            value: Decimal = simulator.get_portfolio_value()
            print(f"Current Portfolio Value: {value}")

            # Update previous prices for next iteration
            prev_lkoh_price = lkoh.price
            prev_sber_price = sber.price

        print("Market Simulation complete.")
    except Exception as e:
        print(f"An error occurred during the simulation: {e}")


if __name__ == "__main__":
    run_market_simulation()
