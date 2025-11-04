import pytest

from app import app as flask_app  # import the Flask instance, not the submodule


@pytest.fixture(autouse=True)
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.is_json
    assert r.get_json()["ok"] is True


def test_homepage_renders(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"<html" in r.data.lower()


def test_resin_calculation_ok(client):
    payload = {
        "resin_cost_per_l": 30,
        "resin_ml_per_model": 50,
        "resin_waste_factor": 10,
        "cleaning_cost_per_l": 8,
        "cleaning_models_per_l": 40,
        "labour_cost_ph": 15,
        "setup_labour_mins": 10,
        "finishing_labour_mins": 5,
        "electricity_cost_kwh": 0.30,
        "printer_wattage": 120,
        "print_time_hours": 2,
        "packaging_cost": 1,
        "shipping_cost": 3,
        "occupancy_charge_per_hour": 0.5,
        "batch_size": 2,
        "failure_rate": 5,
        "profit_margin": 20,
    }
    r = client.post("/calculate-resin", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert data["success"] is True
    for key in [
        "kwh_used",
        "electricity_cost",
        "resin_cost",
        "postage",
        "labour_cost",
        "occupancy_cost",
        "pre_profit_batch_cost",
        "pre_profit_model_cost",
        "post_profit_batch_cost",
        "post_profit_model_cost",
    ]:
        assert key in data
        assert isinstance(data[key], (int, float))


def test_fdm_calculation_ok(client):
    payload = {
        "filament_cost_per_kg": 20,
        "filament_g_per_model": 60,
        "filament_waste_factor": 5,
        "labour_cost_ph": 15,
        "setup_labour_mins": 10,
        "finishing_labour_mins": 5,
        "electricity_cost_kwh": 0.30,
        "printer_wattage": 150,
        "print_time_hours": 1.5,
        "packaging_cost": 1,
        "shipping_cost": 3,
        "occupancy_charge_per_hour": 0.5,
        "batch_size": 3,
        "failure_rate": 2.5,
        "profit_margin": 25,
    }
    r = client.post("/calculate-fdm", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert data["success"] is True
    for key in [
        "kwh_used",
        "electricity_cost",
        "filament_cost",
        "postage_cost",
        "labour_cost",
        "occupancy_charge_cost",
        "pre_profit_batch_cost",
        "pre_profit_model_cost",
        "post_profit_batch_cost",
        "post_profit_model_cost",
    ]:
        assert key in data
        assert isinstance(data[key], (int, float))


def test_env_default_profit_margin_is_used(monkeypatch, client):
    monkeypatch.setenv("APP_DEFAULT_PROFIT_MARGIN", "37.5")
    # Provide a minimal valid FDM payload and omit profit_margin
    payload = {
        "filament_cost_per_kg": 20,
        "filament_g_per_model": 60,
        "filament_waste_factor": 0,
        "labour_cost_ph": 0,
        "setup_labour_mins": 0,
        "finishing_labour_mins": 0,
        "electricity_cost_kwh": 0.30,
        "printer_wattage": 150,
        "print_time_hours": 1,
        "packaging_cost": 0,
        "shipping_cost": 0,
        "occupancy_charge_per_hour": 0,
        "batch_size": 1,
        "failure_rate": 0,
    }
    r = client.post("/calculate-fdm", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert data["success"] is True
    assert "inputs_used" in data
    assert pytest.approx(float(data["inputs_used"]["profit_margin"]), 0.001) == 37.5


def test_payload_overrides_env_default(monkeypatch, client):
    monkeypatch.setenv("APP_DEFAULT_PROFIT_MARGIN", "10")
    # Provide a minimal valid Resin payload and include explicit profit_margin
    payload = {
        "resin_cost_per_l": 30,
        "resin_ml_per_model": 10,
        "resin_waste_factor": 0,
        "cleaning_cost_per_l": 0,
        "cleaning_models_per_l": 1,
        "labour_cost_ph": 0,
        "setup_labour_mins": 0,
        "finishing_labour_mins": 0,
        "electricity_cost_kwh": 0.30,
        "printer_wattage": 120,
        "print_time_hours": 0.2,
        "packaging_cost": 0,
        "shipping_cost": 0,
        "occupancy_charge_per_hour": 0,
        "batch_size": 1,
        "failure_rate": 0,
        "profit_margin": 55,
    }
    r = client.post("/calculate-resin", json=payload)
    assert r.status_code == 200
    data = r.get_json()
    assert data["success"] is True
    assert "inputs_used" in data
    assert pytest.approx(float(data["inputs_used"]["profit_margin"]), 0.001) == 55.0
