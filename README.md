# Eskom loadshedding sensor
This is a home assistant component that follows the `sensor` component type.

This sensor fetches the current Eskom loadshedding status.

# Installation

Place the contents to the `custom_components` folder, if this does not exist then create one in your configuration directory.

# Configuration
Add the following to your `configuration.yaml` file.

```
sensors:
  - platform: loadshedding
    name: "Eskom loadshedding status"
```
