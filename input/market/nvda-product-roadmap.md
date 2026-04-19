# NVIDIA Product Roadmap & Technology Pipeline
**Sources:** NVIDIA newsroom, Tom's Hardware, DataCenterKnowledge, The Register (Tier 1-6)
**Retrieval Date:** 2026-03-19
**NOTE: This file contains NO current price data (price-blinded)**

---

## Current Architecture: Blackwell (H200/GB200/GB300)

- **Status:** Ramping — "nearly 9 gigawatts of infrastructure on Blackwell deployed and consumed" (Q4 FY2026 call)
- **Key products:** H200, GB200 NVL72, GB300 Ultra
- **Architecture share of Q4 FY2026 DC revenue:** Grace Blackwell = ~two-thirds of Data Center revenue
- **Supply chain:** CoWoS oversubscribed; TSMC priority allocation secured
- **Networking:** NVLink 5, Spectrum-4 Ethernet, ConnectX-8 SuperNIC

---

## Next Generation: Vera Rubin (H2 2026 → 2027)

**Source:** NVIDIA newsroom (Tier 1), GTC 2026 announcement (2026-03-16)

### Vera CPU
- 88 custom ARM cores, 176 threads
- 1.8 TB/s NVLink core-to-core interface to Rubin GPUs

### Rubin GPU (Initial, H2 2026)
- Process: TSMC 3nm
- Memory: HBM4
- Memory bandwidth: 22 TB/s (record-breaking)
- Performance: 50 petaflops FP4 (vs. 20 petaflops Blackwell)
- Inference cost: 10x lower than Blackwell
- Rack: NVL72 (72 Rubin GPUs + 36 Vera CPUs, 1.3M components, liquid cooled)
- Initial samples shipped to Tier-1 CSPs (AWS, Google Cloud, Microsoft Azure, Oracle OCI, CoreWeave, Lambda, Nebius, Nscale)
- Full production: On track for H2 2026

### Rubin Ultra (H2 2027)
- Layout: NVL576 (576 GPUs per rack)
- Performance: 100 petaflops FP4 (2x Rubin), 15 ExaFLOPS inference FP4
- Training compute: 5 ExaFLOPS FP8
- GPU dies per package: 4 (increased density)
- Rack power: 600kW (vs Blackwell ~120kW)

---

## Post-2027 Roadmap: Feynman

- Named after theoretical physicist Richard Feynman
- Announced at GTC 2026 as next architecture after Rubin
- No specifications disclosed yet

---

## New Networking Products (GTC 2026)

- NVLink 6
- ConnectX-9 SuperNIC
- BlueField-4 DPU
- Spectrum-6 Ethernet

---

## Platform Strategy: "Full AI Stack"

GTC 2026 keynote theme: NVIDIA positioning as provider of full AI stack:
1. **Hardware:** GPUs (Blackwell → Rubin → Feynman), CPUs (Vera), networking, storage
2. **Software:** CUDA (20th anniversary noted), NeMo for LLMs, Cosmos for physical AI, Alpamayo for autonomous vehicles
3. **Frameworks:** OpenClaw agentic framework (described as fastest-growing OSS project in history)
4. **Platform verticals:**
   - AI factories (data center inference/training)
   - Autonomous vehicles (BYD, Hyundai, Nissan, Geely, Uber partnership)
   - Industrial robotics (ABB, Universal Robots, KUKA)
   - Sovereign AI (national AI programs)

---

## Supply Chain Timeline for Vera Rubin

| Component | Manufacturer | Status (as of 2026-03-19) |
|-----------|-------------|--------------------------|
| GPU die | TSMC 3nm | Production planned H2 2026 |
| CPU die | TSMC [ESTIMATED] | In development |
| HBM4 | SK Hynix, Samsung | NVIDIA secured majority of supply |
| CoWoS packaging | TSMC | Booked years ahead; NVIDIA priority |
| NVLink 6 | NVIDIA custom | Announced GTC 2026 |
