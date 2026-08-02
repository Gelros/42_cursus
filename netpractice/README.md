*This project has been created as part of the 42 curriculum by guilacol.*

# NetPractice

## Description

NetPractice is an introductory networking project from the 42 curriculum. The goal is to solve a series of small network configuration puzzles in a simulated environment delivered through a web interface.

Each level shows a non-functioning network diagram. The student must fill in IP addresses, subnet masks, gateways and routing table entries on hosts and routers so that the requested communications between machines succeed. The project covers 10 levels of increasing complexity, ranging from basic point-to-point connectivity to multi-router topologies with public/private addressing and Internet access.

By completing this project, the student becomes comfortable with:

- IPv4 addressing
- Subnet masks (decimal and CIDR notation)
- Network and broadcast addresses
- Default gateways and their constraints
- Static routing tables (destination/mask and next-hop)
- The distinction between hosts, switches and routers

## Instructions

### Running the training interface

1. Extract the `net_practice` folder anywhere on the machine.
2. From inside that folder, launch the training interface:

```sh
./run.sh
```

If `run.sh` does not work, the project can be served manually with Python:

```sh
python3 -m http.server 49242
```

Then open `http://localhost:49242` in a browser.

### Working through the levels

- On the welcome page, the **intra login must be entered** in the "Training" tab. The simulator uses it to generate the random values that the moulinette will replay during evaluation.
- For each level, edit the unshaded fields (IPs, masks, routes, gateways) until **Check again** returns OK on every goal.
- Click **Get my config** to download the configuration of the current level. The file must be saved before moving on; the **Next level** button only appears once the level is solved.

### Submission

The repository root contains:

- A configuration file for each of the 10 levels, exported with **Get my config**.
- This `README.md`.

The 10 configuration files must be placed at the **root of the repository**, one per level. They are the only files evaluated during the defense (in addition to live resolution of three random levels).

During the defense, three random levels must be solved live, in a limited amount of time, without external tools. A simple calculator such as `bc` is the only thing allowed.

## Resources

### Networking concepts studied

- **TCP/IP addressing**: structure of an IPv4 address as 32 bits / 4 octets, the role of each octet, dotted-decimal notation.
- **Subnet masks**: continuous block of 1s followed by 0s, decimal and CIDR (`/n`) notation, computation of network address, broadcast address, and usable host range.
- **Default gateway**: the next-hop a host uses to reach destinations outside its own subnet; must be an IP in the same subnet as the interface that uses it, and must correspond to an actual router interface.
- **Routers**: layer-3 devices with multiple interfaces, each in a different subnet; forward packets between subnets according to their routing table.
- **Switches**: layer-2 devices that forward Ethernet frames inside a single subnet; have no IP address of their own in this project.
- **Static routes**: explicit `destination_network/mask => gateway` entries; the simulator picks the first matching route in order; a default route is written `0.0.0.0/0`.
- **Private vs public addressing**: RFC 1918 ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) and why the Internet does not route them.
- **OSI layers**: the project mainly exercises layer 2 (Ethernet, switches) and layer 3 (IP, routers); understanding the separation helps when reasoning about which device makes which decision.

### External references

- Cisco IPv4 addressing and subnetting documentation.
- RFC 791 (Internet Protocol).
- RFC 1918 (Address Allocation for Private Internets).
- "TCP/IP Illustrated, Volume 1" by W. Richard Stevens for deeper background.
- The simulator source files in `net_practice/js/` (`sim.js`, `show.js`, `levelN.js`) for understanding how the level checker actually evaluates configurations.

### Use of AI

AI assistance was used as a learning aid, with the following scope:

- Explaining networking concepts (subnet math, gateway rules, routing decisions) with concrete examples drawn from the levels of this project.
- Debugging individual levels by analysing simulator logs and proposing fixes when a goal failed.
- Cross-checking my reasoning on tricky levels (especially levels involving constrained gateways and multi-router topologies).

AI was not used to generate the level configurations blindly. Every IP, mask, route and gateway submitted in the configuration files was understood, justified and verified by re-running **Check again** in the simulator. The defense requires being able to solve random levels live, so the goal of the AI-assisted phase was to build durable mental models, not to copy answers.
