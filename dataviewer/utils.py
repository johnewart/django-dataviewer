import html_table

class Table:
	"""
	This class is a class that generates a table object for use to display 
	collections of data. Allows for formatting of data, headers, and data.
	"""
	def __init__(self, title):
		self.name = title
	
	def fmt_date(self, s):
		if not s:
			return ''
		return s.strftime('%b %d, %Y')
	
	def fmt_str_date(self, s):
		if not s:
			return ''
		return	datetime.datetime.strptime(s, '%Y%m%d').strftime('%b %d, %Y')
	
	def fmt_datetime(self, s):
		if not s:
			return ''
		return s.strftime('%b %d, %Y	%H:%M %p')
	
	def fmt_amount(self, s):
		return comma_sep.fmt('$%.2f', float(s))
	
	def generate(self, table, iter=1):
		if not table:
			return
		
		HEADER, VALUE, FORMAT = range(3)
		
		if type(table[0]) != type([]):
			table = [table]
		
		rows = [[ i[HEADER] for i in table[0] ]]
		for row in table:
			cols = []
			for col in row:
				col = list(col)
				if len(col) > 2:
					if col[FORMAT] == DATE:
						col[VALUE] = self.fmt_date(col[VALUE])
					elif col[FORMAT] == SDATE:
						col[VALUE] = self.fmt_str_date(col[VALUE])
					elif col[FORMAT] == TIME:
						col[VALUE] = self.fmt_time(col[VALUE])
					elif col[FORMAT] == TIME:
						col[VALUE] = self.fmt_time(col[VALUE])
					elif col[FORMAT] == AMOUNT:
						col[VALUE] = self.fmt_amount(col[VALUE])
				cols.append(col[VALUE])
			rows.append(cols)
		
		return self.name, html_table.table(rows)
	
	def show(self, title, table, iter=1):
			rows = self.generate(title, table, iter)
			TextTable(sep='| ').show(rows)
			print