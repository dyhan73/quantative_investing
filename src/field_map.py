# 제무제표 항목명과 DB 필드명 매핑
dic_reports = {
    '코드': 'code',
    '종목코드': 'code',
    'rdate': 'rdate',
    '자산총계': 'total_assets',
    '유동자산': 'current_assets',
    '부채총계': 'total_liabilities',
    '자본총계': 'total_equity',
    '매출액': 'net_sales',
    '매출원가': 'cost_of_sales',
    '매출총이익': 'gross_profit',
    '발표영업이익': 'operating_income',
    '영업이익': 'operating_income',
    '순이익': 'ongoing_operating_income',
    '당기순이익': 'ongoing_operating_income',
    '반기순이익': 'ongoing_operating_income',
    '분기순이익': 'ongoing_operating_income',
    '영업현금흐름': 'cash_flows_from_operatings',
    '영업활동으로인한현금흐름': 'cash_flows_from_operatings',
    '유동비율': 'current_ratio',
    '부채비율': 'debt_to_equity_ratio'
}

dic_companies = {
    '코드': 'code',
    '종목코드': 'code',
    '시장': 'market',
    '회사명': 'company',
    '종목명': 'company',
    '산업코드': 'ind_code',
    '산업명': 'industry'
}