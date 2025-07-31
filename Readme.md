# Resource allocation for OFDMA under IEEE 802.11ax

This project simulates the network traffic under IEEE 802.11ax and test the performance on channel utilisation, fairness and packet reordering problem of different resource unit (RU) allocation algorithms including First in First out (FIFO), Dynamic Programming combined with Timsort (DPT), Updated Dynamic Programming combined with Timsort (UDPT), Greedy algorithm (GrA), Genetic algorithm (GnA) and Simulated Annealing (SA).

# Purpose of this project

The purpose of this project is to compare the performance of different optimisation techniques on RU allocation for downlink traffic uder IEEE 802.11ax OFDMA mechanism.

# Project structure
Resource allocation for OFDMA under IEEE 802.11ax/
├── RunSimulator/  
│   ├── DynamicProgrammingCombinedwithTimsort.py  # The simulator for DPT algorithm. The retransmission rate can be set by the parameter retransmission_rate.  
│   ├── FIFO.py  # The simulator for FIFO algorithm. The retransmission rate can be set by the parameter retransmission_rate.  
│   ├── Genetic Algorithm.py # The simulator for GnA algorithm. The retransmission rate can be set by the parameter retransmission_rate.  
│   ├── GreedyAlgorithm.py  # The simulator for GrA algorithm. The retransmission rate can be set by the parameter retransmission_rate.  
│   ├── ofdma.py  # Simulates a single downlink frame transmission in OFDMA, supporting parallel communication for multiple users.  
│   ├── modulation.py  # This class is a complete QAM modulator suitable for research tasks such as communication simulation, Bit Error Rate (BER) analysis, and integration with OFDMA resource allocation models.  
│   ├── RunFIFO.py  # Run the simulator for FIFO algorithm with different number of users and it will output the average channel utilisation of different numbers of users, average Jain's Fairness index of different numbers of users, average R-value of different number of users and average program runnning time of different number of users.  
│   ├── RunGeneticAlgorithm.py  # Run the simulator for GnA algorithm with different number of users and it will output the average channel utilisation of different numbers of users, average Jain's Fairness index of different numbers of users, average R-value of different number of users and average program runnning time of different number of users.  
│   ├── RunGreedyAlgorithm.py  # Run the simulator for GrA algorithm with different number of users and it will output the average channel utilisation of different numbers of users, average Jain's Fairness index of different numbers of users, average R-value of different number of users and average program runnning time of different number of users.  
│   ├── RunSimulatedAnnealing.py  # Run the simulator for SA algorithm with different number of users and it will output the average channel utilisation of different numbers of users, average Jain's Fairness index of different numbers of users, average R-value of different number of users and average program runnning time of different number of users.  
│   ├── RunSimulatorwithDPT.py  # Run the simulator for DPT algorithm with different number of users and it will output the average channel utilisation of different numbers of users, average Jain's Fairness index of different numbers of users, average R-value of different number of users and average program runnning time of different number of users.  
│   ├── RunSimulatorwithUDPT.py  # Run the simulator for UDPT algorithm with different number of users and it will output the average channel utilisation of different numbers of users, average Jain's Fairness index of different numbers of users, average R-value of different number of users and average program runnning time of different number of users.  
│   ├── SimulatedAnnealing.py  # The simulator for SA algorithm. The retransmission rate can be set by the parameter retransmission_rate.  
│   ├── UpdatedDynamicProgrammingCombinedwithTimsort.py  # The simulator for UDPT algorithm. The retransmission rate can be set by the parameter retransmission_rate.  
├── .gitignore  
└── Readme.md  

# Running the project

The `RunSimulator/` directory contains several simulation scripts, each corresponding to a different RU allocation algorithms. You can run any of them independently using Python. You can set the channel conditions by setting the retransmission_rate which represents the retransmission rate of the packet transmissions in each python file named by different RU allocation algorithms name.

# Library requirements
This project uses Python 3.9.

This project uses the following Python libraries:
numpy
math

# License

This project is licensed under the Apache License 2.0.  
See the [LICENSE](LICENSE) file for details.

# Contact

Maintained by YangYu1006.
