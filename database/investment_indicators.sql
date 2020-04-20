-- PER 구하기
-- PER = 시가총액 / 당기순이익
-- PER = prices.market_cap / reports.ongoing_operating_income
select p.code, p.market_cap, r.ongoing_operating_income
from prices p
join (
    select code, rdate, ongoing_operating_income
    from reports
    where code = p.code
        and
    )
    reports r on p.code=r.code
where p.market_cap is not null


-- joined['PER'] = joined['시가총액'] / joined['당기순이익'] / 1000
-- joined['PSR'] = joined['시가총액'] / joined['매출액'] / 1000
-- joined['PCR'] = joined['시가총액'] / joined['영업현금흐름'] / 1000
-- joined['PBR'] = joined['시가총액'] / joined['자본총계'] / 1000
-- joined['ROA'] = joined['당기순이익'] / joined['자산총계']
-- joined['GPA'] = joined['매출총이익'] / joined['자산총계']