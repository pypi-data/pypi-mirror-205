
import pandas as pd
from sklearn.metrics import log_loss

#Для задач классификации с таргетом 0-1
#Cумма 1 в топ-процент сортированной по предсказанию таблицы позиций делённая на сумму 1 для всей таблицы


def def_baseline(df, target):
	return df[target].sum()


def _uplift(df, target, sort_score, pct, baseline=None):
	
	_baseline = def_baseline(df, target)
	if baseline != None:
		print('baseline is not None, but unknown')
	
	_df = df.sort_values(sort_score, ascending=False)
	pct_len = round(len(df) * pct)
	base_found = _df.head(pct_len)[target].sum()

	return _baseline, ((base_found / _baseline) / pct)


def lloss_up(df, target, score, pct=0.2, baseline=None):
	lloss = log_loss(df[target], df[score])
	base, up = _uplift(df, target, score, pct, baseline=baseline)
	
	table = pd.DataFrame()
	table.index = ['base', 'lloss', 'uplift']
	table[' '] = [base, lloss, up]
	
	print(table)