def calculate_fdm_cost(data):
    try:
        # Extract input values
        filament_cost_per_kg = float(data['filament_cost_per_kg'])
        filament_g_per_model = float(data['filament_g_per_model'])
        filament_waste_factor = float(data['filament_waste_factor']) / 100.0
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
        filament_cost_per_g = filament_cost_per_kg / 1000.0
        total_filament_usage = filament_g_per_model * (1 + filament_waste_factor)
        filament_cost_per_model = total_filament_usage * filament_cost_per_g

        setup_labour_cost = (setup_labour_mins / 60) * labour_cost_ph
        finishing_labour_cost = (finishing_labour_mins / 60) * labour_cost_ph

        kwh_used = (printer_wattage * print_time_hours) / 1000.0
        electricity_cost = kwh_used * electricity_cost_kwh

        occupancy_charge = occupancy_charge_per_hour * print_time_hours

        per_model_cost = filament_cost_per_model + finishing_labour_cost + packaging_cost + shipping_cost
        total_batch_cost = per_model_cost * batch_size + setup_labour_cost + electricity_cost + occupancy_charge

        sellable_models = max(1, batch_size - int(batch_size * failure_rate))
        cost_per_model = total_batch_cost / sellable_models
        final_price = cost_per_model * (1 + profit_margin)

        return {
            "success": True,
            "kwh_used": kwh_used,
            "electricity_cost": electricity_cost,
            "filament_cost": filament_cost_per_model * batch_size,
            "postage_cost": packaging_cost * batch_size + shipping_cost * batch_size,
            "labour_cost": setup_labour_cost + finishing_labour_cost * batch_size,
            "occupancy_charge_cost": occupancy_charge,
            "pre_profit_batch_cost": total_batch_cost,
            "pre_profit_model_cost": per_model_cost,
            "post_profit_batch_cost": total_batch_cost * (1 + profit_margin),
            "post_profit_model_cost": cost_per_model * (1 + profit_margin),
        }

    except Exception as e:
        return {"success": False, "Error in filament cost calculation": str(e)}
