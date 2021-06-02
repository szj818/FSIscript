Open(CouplingStep = 100)
DatamodelRoot().CouplingControl.AnalysisType.DurationControl.EndTime = '15 [s]'

# DatamodelRoot().CouplingParticipant['Solution 1'].ExecutionControl.AdditionalArguments = '-t 2 -mpi=intel'
# DatamodelRoot().OutputControl.Option = 'StepInterval'
# DatamodelRoot().OutputControl.OutputFrequency = '50'
# PartitionParticipants(AlgorithmName = 'SharedAllocateMachines',NamesAndFractions = [('Solution', 1.0/2.0),('Solution 1', 2.0/2.0)], MachineList = [{'machine-name' : 'DESKTOP', 'core-count' : 2}])

StartParticipants()

Solve()

