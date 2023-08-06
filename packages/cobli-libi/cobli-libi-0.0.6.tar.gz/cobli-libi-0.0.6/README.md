# cobli-libi

## About the project

This package generates dataframes using [Cobli's public API](https://docs.cobli.co) as data source.

It was created to enhance the experience of anyone who needs easy-to-use data from his/her Cobli fleet.

Data available in this package:

- Devices
- Checklists
- Proofs of conclusion
- Incidents
- Costs
- Vehicle performance
- Driver performance

### Built with

- [Python](https://www.python.org/)

## Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

`pip install cobli-libi`

## Usage

```python
from datetime import datetime, timedelta
from libi.dataframes import get_devices_data, get_pocs_data, \
    get_costs_data, get_incidents_data, get_checklist_data, \
    get_driver_performance_data, get_vehicle_performance_data

fleet_data = {'Fleet Name': '<fleet_api_key>', 'Another Fleet': '<another_fleet_api_key'}
start_datetime = datetime.now() - timedelta(days=5)
end_datetime = datetime.now()

devices = get_devices_data(fleet_data)
checklists = get_checklist_data(fleet_data)
proofs_of_conclusion = get_pocs_data(fleet_data, start_datetime, end_datetime)
costs = get_costs_data(fleet_data, start_datetime, end_datetime)
incidents = get_incidents_data(fleet_data, start_datetime, end_datetime)
vehicle_performance = get_vehicle_performance_data(fleet_data, start_datetime, end_datetime)
driver_performance = get_driver_performance_data(fleet_data, start_datetime, end_datetime)
```

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Deploy

This project is in [Pypi](https://pypi.org/manage/project/cobli-libi/releases/).

In order to deploy this project, the first action needed is bump the version in the file `setup.py`.

Then, you will have to install build with this command:

`python3 -m pip install --upgrade build`

After this, you will need to build the project with this command:

`python3 -m build`

Then, you will have to install twine with this command:

`python3 -m pip install --upgrade twine`.

Finally, you can deploy in pypi using this command:

`python3 -m twine upload dist/*`

The credentials needed for this command are stored in 1Password by the key _Admin-Pypi_.

## Contact

Project Link: [https://github.com/cobliteam/cobli-libi](https://github.com/cobliteam/cobli-libi)
