# Eskom loadshedding sensor
This is a home assistant component that follows the `sensor` component type.

This sensor fetches the current Eskom loadshedding status.

# Installation

Place the contents into a `custom_components\loadshedding` folder, if either folder do not exist then create them in your configuration directory.

# Configuration
Add the following to your `configuration.yaml` file.

```
sensor:
  - platform: loadshedding
    name: "Eskom loadshedding status"
```
