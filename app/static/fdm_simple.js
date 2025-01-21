document.getElementById("fdm-simple-calculator-form").addEventListener("submit", function (e) {
    e.preventDefault();

    // Input values
    const filamentCostPerKg = parseFloat(document.getElementById("simple_filament_cost_per_kg").value);
    const filamentUsage = parseFloat(document.getElementById("simple_filament_g_per_model").value);
    const filamentWasteFactor = parseFloat(document.getElementById("simple_filament_waste_factor").value);
    const electricityCostKwh = parseFloat(document.getElementById("simple_electricity_cost_kwh").value);
    const printerWattage = parseFloat(document.getElementById("simple_printer_wattage").value);
    const printTimeHours = parseFloat(document.getElementById("simple_print_time_hours").value);

    // Validate inputs
    if (
        !isNaN(filamentCostPerKg) &&
        !isNaN(filamentUsage) &&
        !isNaN(filamentWasteFactor) &&
        !isNaN(electricityCostKwh) &&
        !isNaN(printerWattage) &&
        !isNaN(printTimeHours)
    ) {
        // Filament cost calculation
        const totalFilamentUsage = filamentUsage * (1 + filamentWasteFactor / 100);
        const totalFilamentCost = (filamentCostPerKg / 1000) * totalFilamentUsage;

        // Electricity cost calculation
        const kwhUsed = (printerWattage * printTimeHours) / 1000;
        const totalElectricityCost = kwhUsed * electricityCostKwh;

        // Total cost
        const totalCost = totalFilamentCost + totalElectricityCost;

        // Output results
        document.getElementById("result-filament-cost").textContent = `£${totalFilamentCost.toFixed(2)}`;
        document.getElementById("result-electricity-cost").textContent = `£${totalElectricityCost.toFixed(2)}`;
        document.getElementById("result-kwh-used").textContent = `${kwhUsed.toFixed(2)} kWh`;
        document.getElementById("result-total-cost").textContent = `£${totalCost.toFixed(2)}`;
    } else {
        alert("Please enter valid numbers!");
    }
});
