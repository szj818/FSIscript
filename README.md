## 说明
`fsi.bat`与`fsi.sh`分别为windows与linux下的执行脚本，`fsi.lsf`,`fsi.pbs`,`fsi.slurm`分别是几个作业调度系统LSF、PBS、Slurm的提交脚本。上述几个脚本在执行前需要根据自己的情况修改NPF(Fluent使用核数)、NPA(Mechanical使用核数)，并行方式使用的是`SharedAllocateMachines`,也即共用节点和核心，跨节点运行未考虑。变量FLUID与STRUCT同样要根据实际情况修改为是Solution 1还是Solution。文件夹tutorial提供了算例供试验。

下文为参照官方帮助文档ANSYS SystemCoupling2.0进行的总结，已发布至[SunBlog](https://www.flameszj.top/System-Coupling-2-0/ ),建议直接阅读官方ANSYS帮助文档。

## Working with the System Coupling Data Model
`System Coupling Data Model Settings`包含以下四个部分：`CouplingControl` `OutputControl` `CouplingInterface` `CouplingParticipant`

## Setting Up a Coupled Analysis in Workbench for a Command-Line Run

1. Create a directory structure.
2. Set up the coupled analysis.
注：对于Fluent来说就是要设置一个或多个边界条件，并设置动网格，Calculate下面的时间步长和时间步数不起作用，会被SC中的设置覆盖；
    对于Mechanical来说就是要设置一个System Coupling Region，并注意一些其他设置（`End Time Specification`、`Ramping of Data-Transfer Loads`、`Ramping of Loads Within Mechanical`、`Output Controls`
），
3. Generate participants' solver input files.
  注意：Fluent中的input file需要在更新Workbench Solution之前 产生
4. Export a System Coupling SCI file.
  注意：在早前版本的Workbench下导出的SCI文件可能不含<ParticipantType>这一标签，这时就需要手动加入

## Setting Up a Command-Line Coupled Analysis
### Preparing for a Coupled Analysis
1. 准备一个耦合分析的目录结构
2. 完成各个部件的设置
注：对于Fluent来说就是要设置一个或多个边界条件，并设置动网格，Calculate下面的时间步长和时间步数不起作用，会被SC中的设置覆盖；
    对于Mechanical来说就是要设置一个System Coupling Region
3. 额外的组件设置
包括：Compatible material properties、Compatible topological properties、Appropriate motion definitions
4. 生成各组件文件，包括各组件的输入文件和scp文件

### Creating a Coupled Analysis
#### Using the System Coupling Command-Line Interface (CLI)
打开Shell，根据操作系统的不同执行以下命令：
```bat
"%AWP_ROOT195%\SystemCoupling\bin\systemcoupling"
```
```shell
"$AWP_ROOT195/SystemCoupling/bin/systemcoupling"
```

#### Getting Help in the System Coupling CLI
```bat
"%AWP_ROOT195%\SystemCoupling\bin\systemcoupling" --help 
```
```Python
help(Initialize)
```

### Loading the Participants
```Python
LoadParticipants(InputFiles = ["mechanical.scp", "fluent.scp"])
```
随后会输出scp文件中的信息：` CouplingControl`、`OutputControl`、`CouplingParticipant`
Tip：To load a single participant, you can use the `AddParticipant` command.

### Adding a Coupling Interface
运行命令`AddInterface`以添加耦合交界面，This command allows you to create one interface at a time by specifying the internal object names of participants and regions to be to included in the interface.
Sample：
```python
AddInterface(SideOneParticipantName = ["AEDT-1"], SideOneRegionNames = ["Volume5"], SideTwoParticipantName = ["MAPDL-2"], SideTwoRegionNames = ["FVIN_1"])
```
Tip: To specify participants and regions by object display names, use the AddInterfaceByDisplayName command.

### Adding a Data Transfer
To create a data transfer between the sides of an existing interface, run the `AddDataTransfer` command.This command allows you to create a data transfer by specifying the interface, the target side of the transfer, and variables to be associated with each side of the interface. To create a two-way data transfer on an interface, you must run this command twice, once for each direction.
After creating data transfers, you can run the `GetErrors` command to verify that no errors were introduced.
```python
AddDataTransfer(Interface = "Interface-1",TargetSide = "Two",SideOneVariable = "Loss",SideTwoVariable = "HGEN")
```

### Setting Geometry Transformations for Models with Different Orientations

## Running a Command-Line Coupled Analysis

### Starting the Participants
运行
```Python
StartParticipants()
```
`StartParticipants()`为可选参数，可以忽略此参数直接运行之后的`Solve` `Initialize` `Step`等命令，软件会自动地启动各个组件（除非是在`ExecutionControl`设置为`ExternallyManaged`这种情况下，软件无法自动启动各个组件），不过`StartParticipants()`可以提供更多的控制选项

### Starting the Solution
运行
```Python
Solve()
```

### Monitoring Solution Progress
求解开始后，耦合求解的输出会存到Transcript和Log File中

### Reviewing Coupled Analysis Output
求解好后，可以查看分析输出文件并进行相应的后处理

## Advanced Workflows for Command—Line System Coupling
### Saving a Command-Line Coupled Analysis
耦合分析会自动存到两个HDF5文件里面，如果需要手动保存，可以使用`Save`命令。默认情况下，上次完成的结果文件会保存到`SyC`目录下面

### Stopping a Command-Line Coupled Analysis Run
1. 在交互模式下，使用`Shutdown`命令来停止，这是一种干净的Shutdown，可以生成一个Restart point
2. 在命令行模式下，可以在System Coupling工作目录下面创建一个名为scStop的文件来Interrupt或者Aboort计算

### Restarting a Command-Line Coupled Analysis Run
#### Creation of Restart Points for Command-Line System Coupling
Restart points可以以在以下几种情况下产生：
1. 可以通过`outputControl` data model settings指定
2. 通过`CreateRestartPoint`交互式命令指定 
3. 分析干净退出时

#### Restarting a Command-Line Run from the Final Result
1. 在System Coupling控制台，运行`open`命令，System Coupling会默认找到最新的coupling step，载入需要的数据并从该时间步重新开始
2. 如果之前的分析已经求解完，可以通过使用`DurationControl`设置来延长分析
3. 如果需要修改设置，可以在此时进行修改，在重启之前的设置都会写入到`Settings`文件并在下次重算时使用
4. 使用你自己喜欢的求解过程（使用`Solve`命令或者是交互式的求解命令） 

#### Restarting a Command-Line Run from an Intermediate Result
1. 运行带有`CouplingStep`参数的`open`命令（注意，当从一个较早的重算点重算时，这之后的重算点都会被删除，如果还要这些重算点，可以在不同的目录下面保存重算点文件和Settings文件）
2. 如果需要修改设置，可以在此时进行修改，在重启之前的设置都会写入到`Settings`文件并在下次重算时使用
3. 使用你自己喜欢的求解过程（使用`Solve`命令或者是交互式的求解命令） 

### Using Interactive Solve Commands
一些主要的交互式命令：
```Python
PrintSetup
Initialize
Step
CreateRestartPoint
Shutdown
```

### Using Parallel Processing Capabilities

#### 并行运行流固耦合的流程
1. Set up your analysis
2. (Optional) To start System Coupling in parallel mode, use the parallel-specific startup options
3. Set up your coupled analysis
4. Edit your data model settings.
5. (Optional) To run a coupling participant in parallel mode, use the `ParallelArguments` ExecutionControl setting to specify details of the participant's execution
Tip：Parallel arguments are not specified in the participant's SCP file and must be entered directly into the data model.
6. (Optional) Use the `PartitionParticipants` command to specify how the participants are partitioned across compute resources. For more information, see Using Parallel Processing Capabilities.
7. Run the solution.

#### Parallel Processing for System Coupling
```bat
 "%AWP_ROOT195%\SystemCoupling\bin\systemcoupling" -t<NPROCS> [-p <INTERCONNECT>] 
[--mpi=<MPI>] [-cnf=<HOSTFILE>] 
```

```shell
$AWP_ROOT195/SystemCoupling/bin/systemcoupling" -t<NPROCS> [-p <INTERCONNECT>] 
[--mpi=<MPI>] [-cnf=<HOSTFILE>] 
```

#### Participant Partitioning Examples
```python
PartitionParticipants(AlgorithmName = 'SharedAllocateMachines',NamesAndFractions = [('PARTICIPANT-1', 1.0), ('PARTICIPANT-2', 1.0),('PARTICIPANT-3', 1.0/5.0)]),MachineList = [{'M0' : 'host1', 'core-count' : 12},{'M1' : 'host2', 'core-count' : 12},{'M2' : 'host3', 'core-count' : 12},{'M3' : 'host4', 'core-count' : 7},{'M4' : 'host5', 'core-count' : 6},{'M5' : 'host6', 'core-count' : 3},{'M6' : 'host7', 'core-count' : 3},{'M7' : 'host8', 'core-count' : 1},{'M8' : 'host9', 'core-count' : 1}])
```

### Executing a Command-Line Run of a Coupled Analysis Set Up in Workbench
You can execute a command-line run of a coupled analysis that was set up in Workbench.The execution process is similar to that of an analysis to be run from the command line, except that you'll:
1. populate the data model with a System Coupling SCI file instead of multiple SCP files, and
2. set execution controls in the data model (because the SCI file doesn't provide this information).
Note: 
    1. The use of both SCI and SCP files in the same analysis is not supported.
    2. Restarts are not supported if the default participant names (as assigned in the SCI file: Solution, Solution 1, etc.) have been changed.

To run your Workbench setup from the command line, perform the following steps:
1. Start System Coupling as described in Using the System Coupling Command-Line Interface (CLI).
2. Import the SCI file by running the `ImportSystemCouplingInputFile`.
```python
ImportSystemCouplingInputFile(FilePath = 'scInput.sci')
```
3. To provide information not included in the SCI file, edit each participant's ExecutionControl settings in the data model:
    1. Set `WorkingDirectory` to the participant's coupling working directory.
    2. Set InitialInput to the name of the participant's solver input file.
    Example:Set execution controls for two participants
```python
DatamodelRoot().CouplingParticipant['Solution'].ExecutionControl.InitialInput = 'structural.dat'
 DatamodelRoot().CouplingParticipant['Solution'].ExecutionControl.WorkingDirectory = 'Struct'
DatamodelRoot().CouplingParticipant['Solution 1'].ExecutionControl.InitialInput = 'fluidFlow.cas'
DatamodelRoot().CouplingParticipant['Solution 1'].ExecutionControl.WorkingDirectory = 'Fluid'
```
4. Run the coupled analysis as described in Running a Command-Line Coupled Analysis.
5. If desired, restart the coupled analysis as described in Restarting a Command-Line Coupled Analysis Run. Do not reissue the ImportSystemCouplingInputFile command.

## System Coupling Related Settings in Mechanical
1. End Time Specification
2. Ramping of Data-Transfer Loads
3. Ramping of Loads Within Mechanical
4. Output Controls

## 脚本示例
本脚本是在Workbench图形界面中将各部件中设置好后，导出各部件相应的输入文件和`sci`文件，再在命令行模式下进行计算。
首先打开System Coupling CLI
Windows：
```bat
"%AWP_ROOT195%\SystemCoupling\bin\systemcoupling"
```
Linux:
```shell
"$AWP_ROOT195/SystemCoupling/bin/systemcoupling"
```

```Python
# Import the SCI file
ImportSystemCouplingInputFile(FilePath = 'coupling.sci')


# To provide information not included in the SCI file, edit each participant's ExecutionControl settings in the data model:
DatamodelRoot().CouplingParticipant['Solution'].ExecutionControl.InitialInput = 'struct.dat'
DatamodelRoot().CouplingParticipant['Solution'].ExecutionControl.WorkingDirectory = 'Struct'

DatamodelRoot().CouplingParticipant['Solution 1'].ExecutionControl.WorkingDirectory = 'Fluid'
DatamodelRoot().CouplingParticipant['Solution 1'].ExecutionControl.InitialInput = 'fluidFlow.jou'

DatamodelRoot().CouplingParticipant['Solution 1'].ExecutionControl.InitialInput = 'fluidFlow.cas'
DatamodelRoot().CouplingParticipant['Solution 1'].ExecutionControl.AdditionalArguments = '-t 2 -mpi=intel'

# Parallel Settings
PartitionParticipants(AlgorithmName = 'SharedAllocateMachines',NamesAndFractions = [('Solution', 0.5),('Solution 1', 1.0)], MachineList = [{'machine-name' : 'DESKTOP-szj', 'core-count' : 2}])

#  Starting the Participants
StartParticipants()


# Starting the Solution
Solve()

# Restart the Solution
Open(FilePath = 'WorkingDirectoryWithResults', CouplingStep = 6)
DatamodelRoot().CouplingControl.AnalysisType.DurationControl.EndTime = '15 [s]'
# 另外各个部件也要完成相应的时间延长设置，如Mechanical中将struct.dat中的time延长。
```
一些可选命令
```Python
DatamodelRoot().CouplingControl.PrintState()
DatamodelRoot().CouplingParticipant.GetChildNames()
DatamodelRoot().CouplingParticipant['Solution 1'].ExecutionControl.PrintState()

DatamodelRoot().OutputControl.Option = 'StepInterval'
DatamodelRoot().OutputControl.OutputFrequency = '50'
DatamodelRoot().CouplingControl.AnalysisType.DurationControl.EndTime = '10 [s]'
DatamodelRoot().CouplingControl.AnalysisType.StepControl.TimeStepSize = '1.0 [s]'

GetErrors()
GetErrorsXML()
```

