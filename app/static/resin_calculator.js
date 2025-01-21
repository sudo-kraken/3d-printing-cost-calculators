document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("resin-calculator-form").addEventListener("submit", async function (e) {
        e.preventDefault();

        const data = {
            resin_cost_per_l: parseFloat(document.getElementById("resin_cost_per_l").value),
            resin_ml_per_model: parseFloat(document.getElementById("resin_ml_per_model").value),
            resin_waste_factor: parseFloat(document.getElementById("resin_waste_factor").value),
            cleaning_cost_per_l: parseFloat(document.getElementById("cleaning_cost_per_l").value),
            cleaning_models_per_l: parseFloat(document.getElementById("cleaning_models_per_l").value),
            labour_cost_ph: parseFloat(document.getElementById("labour_cost_ph").value),
            setup_labour_mins: parseFloat(document.getElementById("setup_labour_mins").value),
            finishing_labour_mins: parseFloat(document.getElementById("finishing_labour_mins").value),
            electricity_cost_kwh: parseFloat(document.getElementById("electricity_cost_kwh").value),
            printer_wattage: parseFloat(document.getElementById("printer_wattage").value),
            print_time_hours: parseFloat(document.getElementById("print_time_hours").value),
            packaging_cost: parseFloat(document.getElementById("packaging_cost").value),
            shipping_cost: parseFloat(document.getElementById("shipping_cost").value),
            batch_size: parseFloat(document.getElementById("batch_size").value),
            failure_rate: parseFloat(document.getElementById("failure_rate").value),
            occupancy_charge_per_hour: parseFloat(document.getElementById("occupancy_charge_per_hour").value),
            profit_margin: parseFloat(document.getElementById("profit_margin").value),
        };

        const response = await fetch("/calculate-resin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (result.success) {
            document.getElementById("result-kwh-used").textContent = `${result.kwh_used.toFixed(2)} kWh`;
            document.getElementById("result-electricity-cost").textContent = `£${result.electricity_cost.toFixed(2)}`;
            document.getElementById("result-resin-cost").textContent = `£${result.resin_cost.toFixed(2)}`;
            document.getElementById("result-postage").textContent = `£${result.postage.toFixed(2)}`;
            document.getElementById("result-labour-cost").textContent = `£${result.labour_cost.toFixed(2)}`;
            document.getElementById("result-occupancy-cost").textContent = `£${result.occupancy_cost.toFixed(2)}`;
            document.getElementById("result-pre-profit-batch").textContent = `£${result.pre_profit_batch_cost.toFixed(2)}`;
            document.getElementById("result-pre-profit-model").textContent = `£${result.pre_profit_model_cost.toFixed(2)}`;
            document.getElementById("result-post-profit-batch").textContent = `£${result.post_profit_batch_cost.toFixed(2)}`;
            document.getElementById("result-post-profit-model").textContent = `£${result.post_profit_model_cost.toFixed(2)}`;
        } else {
            alert(`Error: ${result.error}`);
        }
    });
});
