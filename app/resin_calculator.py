def calculate_resin_cost(data):
    try:
        # Extract input values
        resin_cost_per_l = float(data['resin_cost_per_l'])
        resin_ml_per_model = float(data['resin_ml_per_model'])
        resin_waste_factor = float(data['resin_waste_factor']) / 100.0
        cleaning_cost_per_l = float(data['cleaning_cost_per_l'])
        cleaning_models_per_l = float(data['cleaning_models_per_l'])
        labour_cost_ph = float(data['labour_cost_ph'])
        setup_labour_mins = float(data['setup_labour_mins'])
        finishing_labour_mins = float(data['finishing_labour_mins'])
        electricity_cost_kwh = float(data['electricity_cost_kwh'])
        printer_wattage = float(data['printer_wattage'])
        print_time_hours = float(data['print_time_hours'])
        packaging_cost = float(data['packaging_cost'])
        shipping_cost = float(data['shipping_cost'])
        batch_size = int(data['batch_size'])
        failure_rate = float(data['failure_rate']) / 100.0
        occupancy_charge_per_hour = float(data['occupancy_charge_per_hour'])
        profit_margin = float(data['profit_margin']) / 100.0

        # Calculations
        resin_cost_per_ml = resin_cost_per_l / 1000.0
        total_resin_usage = resin_ml_per_model * (1 + resin_waste_factor)
        resin_cost_per_model = total_resin_usage * resin_cost_per_ml

        cleaning_cost_per_model = cleaning_cost_per_l / cleaning_models_per_l

        setup_labour_cost = (setup_labour_mins / 60) * labour_cost_ph
        finishing_labour_cost = (finishing_labour_mins / 60) * labour_cost_ph

        kwh_used = (printer_wattage * print_time_hours) / 1000.0
        electricity_cost = kwh_used * electricity_cost_kwh

        occupancy_charge = occupancy_charge_per_hour * print_time_hours

        per_model_cost = resin_cost_per_model + cleaning_cost_per_model + finishing_labour_cost + packaging_cost + shipping_cost
        total_batch_cost = per_model_cost * batch_size + setup_labour_cost + electricity_cost + occupancy_charge

        sellable_models = max(1, batch_size - int(batch_size * failure_rate))
        cost_per_model = total_batch_cost / sellable_models
        final_price = cost_per_model * (1 + profit_margin)

        return {
            "success": True,
            "kwh_used": kwh_used,
            "electricity_cost": electricity_cost,
            "resin_cost": resin_cost_per_model * batch_size,
            "postage": packaging_cost * batch_size + shipping_cost * batch_size,
            "labour_cost": setup_labour_cost + finishing_labour_cost * batch_size,
            "occupancy_cost": occupancy_charge,
            "pre_profit_batch_cost": total_batch_cost,
            "pre_profit_model_cost": per_model_cost,
            "post_profit_batch_cost": total_batch_cost * (1 + profit_margin),
            "post_profit_model_cost": cost_per_model * (1 + profit_margin),
        }
        
    except Exception as e:
        raise ValueError(f"Error in resin cost calculation: {e}")
