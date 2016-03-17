### Designs and Mocks
Right now we're implementing for the case where traffic is prioritized on a
simple metric, for example destination IP address.  When multiple connections
come in, we prioritize connections and blackhole others:
![Scenario](/img/scenario.png)

Ultimately, this is what our first prototype will look like at a high level:
![Implementation](/img/implementation.png)

### Web UI
We have a simple web UI that we can use to generate different types of traffic.
While we can use libraries (like `scapy`) to generate traffic for unit testing
and performance testing, it's helpful to have a UI where we can manually create
traffic.  [Web UI]( https://berkeley-mosc.github.io/MOSC/)
