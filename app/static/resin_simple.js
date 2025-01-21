document.getElementById("resin-simple-calculator-form").addEventListener("submit", function (e) {
    e.preventDefault();

    // Input values
    const resinCost = parseFloat(document.getElementById("simple_resin_cost_per_l").value);
    const resinUsage = parseFloat(document.getElementById("simple_resin_ml_per_model").value);
    const resinWasteFactor = parseFloat(document.getElementById("simple_resin_waste_factor").value);
    const electricityCostKwh = parseFloat(document.getElementById("simple_electricity_cost_kwh").value);
    const printerWattage = parseFloat(document.getElementById("simple_printer_wattage").value);
    const printTimeHours = parseFloat(document.getElementById("simple_print_time_hours").value);

    // Validate inputs
    if (
        !isNaN(resinCost) &&
        !isNaN(resinUsage) &&
        !isNaN(resinWasteFactor) &&
        !isNaN(electricityCostKwh) &&
        !isNaN(printerWattage) &&
        !isNaN(printTimeHours)
    ) {
        // Resin cost calculation
        const totalResinUsage = resinUsage * (1 + resinWasteFactor / 100);
        const totalResinCost = (resinCost / 1000) * totalResinUsage;

        // Electricity cost calculation
        const kwhUsed = (printerWattage * printTimeHours) / 1000;
        const totalElectricityCost = kwhUsed * electricityCostKwh;

        // Total cost
        const totalCost = totalResinCost + totalElectricityCost;

        // Output results
        document.getElementById("result-resin-cost").textContent = `£${totalResinCost.toFixed(2)}`;
        document.getElementById("result-electricity-cost").textContent = `£${totalElectricityCost.toFixed(2)}`;
        document.getElementById("result-kwh-used").textContent = `${kwhUsed.toFixed(2)} kWh`;
        document.getElementById("result-total-cost").textContent = `£${totalCost.toFixed(2)}`;
    } else {
        alert("Please enter valid numbers!");
    }
});
