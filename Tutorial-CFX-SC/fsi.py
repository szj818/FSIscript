import os

HOST=os.getenv('NODES')
NPF=int(os.getenv('NPF'))
NPA=int(os.getenv('NPA'))
NP=int(os.getenv('NP'))
FLUID=os.getenv('FLUID')
STRUCT=os.getenv('STRUCT')

ImportSystemCouplingInputFile(FilePath = 'coupling.sci')
DatamodelRoot().CouplingParticipant[STRUCT].ExecutionControl.InitialInput = 'struct.dat'
DatamodelRoot().CouplingParticipant[STRUCT].ExecutionControl.WorkingDirectory = 'Struct'
DatamodelRoot().CouplingParticipant[FLUID].ExecutionControl.WorkingDirectory = 'Fluid'
DatamodelRoot().CouplingParticipant[FLUID].ExecutionControl.InitialInput = 'Fluid.def'

DatamodelRoot().CouplingParticipant[FLUID].ExecutionControl.AdditionalArguments = ''
# DatamodelRoot().CouplingParticipant[FLUID].ExecutionControl.AdditionalArguments = '-t %d '%(NPF)+'-mpi=intel'

PartitionParticipants(AlgorithmName = 'SharedAllocateMachines',NamesAndFractions = [(FLUID, NPF),(STRUCT, NPA)], MachineList = [{'machine-name' : HOST, 'core-count' : NP}])

StartParticipants()

Solve()