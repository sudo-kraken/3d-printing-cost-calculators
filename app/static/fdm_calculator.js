document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("filament-calculator-form").addEventListener("submit", async function (e) {
        e.preventDefault();

        // Gather input values
        const data = {
            filament_cost_per_kg: parseFloat(document.getElementById("filament_cost_per_kg").value),
            filament_g_per_model: parseFloat(document.getElementById("filament_g_per_model").value),
            filament_waste_factor: parseFloat(document.getElementById("filament_waste_factor").value),
            electricity_cost_kwh: parseFloat(document.getElementById("electricity_cost_kwh").value),
            printer_wattage: parseFloat(document.getElementById("printer_wattage").value),
            print_time_hours: parseFloat(document.getElementById("print_time_hours").value),
            labour_cost_ph: parseFloat(document.getElementById("labour_cost_ph").value),
            setup_labour_mins: parseFloat(document.getElementById("setup_labour_mins").value),
            finishing_labour_mins: parseFloat(document.getElementById("finishing_labour_mins").value),
            packaging_cost: parseFloat(document.getElementById("packaging_cost").value),
            shipping_cost: parseFloat(document.getElementById("shipping_cost").value),
            batch_size: parseInt(document.getElementById("batch_size").value),
            failure_rate: parseFloat(document.getElementById("failure_rate").value),
            occupancy_charge_per_hour: parseFloat(document.getElementById("occupancy_charge_per_hour").value),
            profit_margin: parseFloat(document.getElementById("profit_margin").value),
        };

        const response = await fetch("/calculate-fdm", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (result.success) {
            document.getElementById("result-kwh-used").textContent = `${(result.kwh_used).toFixed(2)} kWh`;
            document.getElementById("result-electricity-cost").textContent = `£${result.electricity_cost.toFixed(2)}`;
            document.getElementById("result-filament-cost").textContent = `£${result.filament_cost.toFixed(2)}`;
            document.getElementById("result-postage").textContent = `£${result.postage_cost.toFixed(2)}`;
            document.getElementById("result-labour-cost").textContent = `£${result.labour_cost.toFixed(2)}`;
            document.getElementById("result-occupancy-cost").textContent = `£${result.occupancy_charge_cost.toFixed(2)}`;
            document.getElementById("result-pre-profit-batch").textContent = `£${result.pre_profit_batch_cost.toFixed(2)}`;
            document.getElementById("result-pre-profit-model").textContent = `£${result.pre_profit_model_cost.toFixed(2)}`;
            document.getElementById("result-post-profit-batch").textContent = `£${result.post_profit_batch_cost.toFixed(2)}`;
            document.getElementById("result-post-profit-model").textContent = `£${result.post_profit_model_cost.toFixed(2)}`;
        } else {
            alert(`Error: ${result.error}`);
        }
    });
});