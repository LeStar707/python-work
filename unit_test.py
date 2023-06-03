import math
from start1 import calculate_package_costs

def test_calculate_package_costs():
    packages = {
        (9080, 1): {'package cost': 265.50, 4024: 88.50, 4025: 88.50, 4026: 88.50},
        (9040, 18): {'package cost': 530.00, 9026: 205.87, 5014: 162.07, 9009: 162.07},
        (9080, 62): {'package cost': 265.50, 4024: 88.50, 4025: 88.50, 4026: 88.50}
    }

    results = {
        4024: {'title': "Сечовина", 'counter': 246, 'cost': 9859.21},
        4025: {'title': "Сечова кислота", 'counter': 355, 'cost': 21265.23},
        4026: {'title': "Тест 4026", 'counter': 100, 'cost': 0},
        9026: {'title': "Тест 9026", 'counter': 1, 'cost': 205.87},
        5014: {'title': "Тест 5014", 'counter': 1, 'cost': 162.07},
        9009: {'title': "Тест 9009", 'counter': 1, 'cost': 162.07}
    }

    calculate_package_costs(packages, results)

    # Verify results after calculation
    assert math.isclose(results[4024]['cost'], 9859.21 + (88.5 / (88.5 + 88.5 + 88.5) * 265.5) + (88.5 / (88.5 + 88.5 + 88.5) * 265.5))
    assert math.isclose(results[4025]['cost'], 21265.23 + (88.5 / (88.5 + 88.5 + 88.5) * 265.5) + (88.5 / (88.5 + 88.5 + 88.5) * 265.5))
    assert math.isclose(results[4026]['cost'], (88.5 / (88.5 + 88.5 + 88.5) * 265.5) + (88.5 / (88.5 + 88.5 + 88.5) * 265.5))
    assert math.isclose(results[9026]['cost'], 205.87 + (205.87 / (205.87 + 162.07 + 162.07)) * 530.00)
    assert math.isclose(results[5014]['cost'], 162.07 + (162.07 / (205.87 + 162.07 + 162.07)) * 530.00)
    assert math.isclose(results[9009]['cost'], 162.07 + (162.07 / (205.87 + 162.07 + 162.07)) * 530.00)
    assert results[4024]['counter'] == 246
    assert results[4025]['counter'] == 355
    assert results[4026]['counter'] == 100

    print("Test passed!")

# Run the test
test_calculate_package_costs()