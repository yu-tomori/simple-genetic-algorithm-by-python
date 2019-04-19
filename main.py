import random
import GeneticAlgorithm
from decimal import *

# 遺伝情報の長さ
GENOM_LENGTH = 100
# 遺伝集団の大きさ
MAX_GENOM_LIST = 100
# 遺伝子選択数
SELECT_GENOM = 20
# 個体突然変異率
INDIVIDUAL_MUTATION = 0.1
# 遺伝子突然変異率
GENOM_MUTATION = 0.1
# 世代数
MAX_GENERATION = 40

def create_genom(length):
 genom_list = []
 for i in range(length):
  genom_list.append(random.randint(0, 1))
 return GeneticAlgorithm.genom(genom_list, 0)
# ランダムで生成した1個体の遺伝子配列をgenomClassのインスタンスとして返す。評価の初期値は0

def evaluation(ga):
 genom_total = sum(ga.getGenom())
 return Decimal(genom_total) / Decimal(len(ga.getGenom()))

def select(ga, elite_length):
 sort_result = sorted(ga, reverse=True, key=lambda u: u.evaluation)
 result = [sort_result.pop(0) for i in range(elite_length)]
 return result

def crossover(ga_one, ga_second):
 # 子孫を格納するリスト
 genom_list = []
 # 入れ替える二点の点を設定します
 cross_one = random.randint(0, GENOM_LENGTH)
 cross_second = random.randint(cross_one, GENOM_LENGTH)
 # 遺伝子を取り出す
 one = ga_one.getGenom()
 second = ga_second.getGenom()
 # 交叉させる
 progeny_one = one[:cross_one] + second[cross_one:cross_second] + one[cross_second:]
 progeny_second = second[:cross_one] + one[cross_one:cross_second] + second[cross_second:]
 # genomClassインスタンスを生成して子孫をリストに格納する
 genom_list.append(GeneticAlgorithm.genom(progeny_one, 0))
 genom_list.append(GeneticAlgorithm.genom(progeny_second, 0))
 return genom_list

def next_generation_gene_create(ga, ga_elite, ga_progeny):
 # 現行世代個体集団の合計分を取り除く
 next_generation_geno = sorted(ga, reverse=False, key=lambda u: u.evaluation)
 for i in range(0, len(ga_elite) + len(ga_progeny)):
  next_generation_geno.pop(0)
 # エリート集団と子孫集団を次世代集団を次世代へ追加します
 next_generation_geno.extend(ga_elite)
 next_generation_geno.extend(ga_progeny)
 return next_generation_geno

def mutation(ga, individual_mutation, genom_mutation):
 ga_list = []
 for i in ga:
  # 個体に対して一定の確率で突然変異が起きる
  if individual_mutation > (random.randint(0, 100) / Decimal(100)):
   genom_list = []
   for i_ in i.getGenom():
    # 個体の遺伝子情報１つ１つに対して突然変異が起きる
    if genom_mutation > (random.randint(0, 100) / Decimal(100)):
     genom_list.append(random.randint(0, 1))
    else:
     genom_list.append(i_)
   i.setGenom(genom_list)
   ga_list.append(i)
  else:
   ga_list.append(i)
 return ga_list

if __name__ == '__main__':
 # 一番最初の現行世代個体集団を生成します
 current_generation_individual_group = [] 
 for i in range(MAX_GENOM_LIST):
  current_generation_individual_group.append(create_genom(GENOM_LENGTH))
 for count_ in range(1, MAX_GENERATION + 1):
  # 現行世代集団の遺伝子を評価し、genomClassに代入します
  for i in range(MAX_GENOM_LIST):
   evaluation_result = evaluation(current_generation_individual_group[i])
   current_generation_individual_group[i].setEvaluation(evaluation_result)
  # エリート個体を選択する
  elite_genes = select(current_generation_individual_group, SELECT_GENOM)
  # エリート遺伝子を交叉させ、リストに格納する
  progeny_gene = []
  for i in range(0, SELECT_GENOM):
   progeny_gene.extend(crossover(elite_genes[i - 1], elite_genes[i]))
  # 次世代個体集団を現行世代、エリート集団、子孫集団から作成します
  next_generation_individual_group = next_generation_gene_create(current_generation_individual_group, elite_genes, progeny_gene)
  # 次世代個体集団全ての個体に突然変異を施します
  next_generation_individual_group = mutation(next_generation_individual_group, INDIVIDUAL_MUTATION, GENOM_MUTATION)
  
  # 1世代の進化的計算が終わり、評価に移る
  # 描く古来の適応度を配列化
  fits = [i.getEvaluation() for i in current_generation_individual_group]
  # 進化結果を評価
  min_ = min(fits)
  max_ = max(fits)
  avg_ = sum(fits) / Decimal(len(fits))
  
  # 現行世代の進化結果を出力
  # print "--------第{}世代".format(count_)
  print('------第%s世代の結果' % str(count_))
  print('  Min:%s' % str(min_))
  print('  Max:%s' % str(max_))
  print('  Avg:%s' % str(avg_))

  # 現行世代を次世代を入れ替える
  current_generation_individual_group = next_generation_individual_group

 # 最終結果を出力
 # print "もっとの優れた個体は{}".format(elite_genes[0].getGenom()) 
 print('最も優れた個体は%s' % str(elite_genes[0].getGenom()))
