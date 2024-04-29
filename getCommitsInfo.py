import sys
import csv
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.hunks_count import HunksCount

columns = ['SHA','Message','DMM_unit_size','DMM_unit_complexity','DMM_unit_interfacing','Churn_count','Churn_max','Churn_avg','Hunks_count','Commit_dist','Diff']
rows = []
count=0
last_n=100

commits = []
for x in Repository(sys.argv[1],only_no_merge=True,order='reverse').traverse_commits():
  if (x.in_main_branch==True):
    count=count+1
    commits.append(x)
    if count == last_n:
      break

in_order = []
for value in range(len(commits)):
  in_order.append(commits.pop())

commits=in_order
i=-1
for commit in commits:
  i+=1
  print('[{}/{}] Mining commit {}.{}'.format(i+1,len(commits),sys.argv[1],commit.hash))
  diff = []
  for m in commit.modified_files:
    diff.append(m.diff_parsed)
      
  if (i>=1):
    metric=CodeChurn(path_to_repo=sys.argv[1],from_commit=commits[i-1].hash,to_commit=commits[i].hash)
    churn_count = metric.count()
    churn_max = metric.max()
    churn_avg = metric.avg()
      
    metric=HunksCount(path_to_repo=sys.argv[1],from_commit=commits[i-1].hash,to_commit=commits[i].hash)
    hunks_count = metric.count()
       
    metric=CommitsCount(path_to_repo=sys.argv[1],from_commit=commits[i-1].hash,to_commit=commits[i].hash)
    commit_dist = metric.count()
       
    rows.append([commit.hash,commit.msg,commit.dmm_unit_size,commit.dmm_unit_complexity,commit.dmm_unit_interfacing,churn_count,churn_max,churn_avg,hunks_count,commit_dist,diff])
  elif (i==0):
    rows.append([commit.hash,commit.msg,commit.dmm_unit_size,commit.dmm_unit_complexity,commit.dmm_unit_interfacing,'','','','','',''])
       
with open(sys.argv[1]+'_results/commits_info.csv', 'a') as csvFile:
  writer = csv.writer(csvFile)
  writer.writerow(columns)
  writer.writerows(rows)
