
set NPA=1
set NP=2
set NPF=2
for /F %%i in ('hostname') do ( set NODES=%%i)
set FLUID=Solution
set STRUCT=Solution 1

"%AWP_ROOT195%\SystemCoupling\bin\systemcoupling" -R fsi.py 


