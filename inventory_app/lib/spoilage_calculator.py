from datetime import datetime, date
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpoilageCalculator:
    def __init__(self):
        self.logger = logger

    def calculate_spoilage_risk(self, expiry_date, avg_temp, days_stored, reliability_score):
        """
        Calculate spoilage risk based on shelf life, average temperature, days stored, and supplier reliability.
        Returns a percentage (0-100).
        """
        try:
            # Convert expiry_date to days remaining
            today = date.today()
            
            if isinstance(expiry_date, str):
                expiry = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            elif hasattr(expiry_date, 'date'):
                expiry = expiry_date.date()
            else:
                expiry = expiry_date
            
            days_to_expiry = (expiry - today).days
            
            # Base risk calculation
            if days_to_expiry <= 0:
                base_risk = 90  # Very high risk if expired
            elif days_to_expiry <= 7:
                base_risk = 70  # High risk if expiring within a week
            elif days_to_expiry <= 30:
                base_risk = 40  # Medium risk if expiring within a month
            else:
                base_risk = max(0, 30 - (days_to_expiry / 10))  # Lower risk for longer shelf life
            
            # Temperature factor (optimal range 2-8°C for most perishables)
            if avg_temp > 25:
                temp_factor = min((avg_temp - 25) * 3, 30)  # High temp increases risk significantly
            elif avg_temp < 2:
                temp_factor = min((2 - avg_temp) * 2, 20)  # Too cold can also damage
            elif 2 <= avg_temp <= 8:
                temp_factor = 0  # Optimal temperature
            else:
                temp_factor = min((avg_temp - 8) * 1.5, 15)  # Slightly above optimal
            
            # Storage duration factor
            storage_factor = min(days_stored * 0.8, 25)
            
            # Supplier reliability factor (lower reliability = higher risk)
            reliability_factor = max(0, (100 - reliability_score) * 0.15)
            
            # Calculate total risk
            total_risk = min(100, base_risk + temp_factor + storage_factor + reliability_factor)
            
            self.logger.info(f"Spoilage risk calculation: {total_risk:.2f}% (days_to_expiry={days_to_expiry}, temp={avg_temp}°C, stored={days_stored} days, reliability={reliability_score}%)")
            
            return round(total_risk, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating spoilage risk: {e}")
            return 50.0  # Return moderate risk as fallback