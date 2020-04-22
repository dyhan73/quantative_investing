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


select * -- code, rdate, net_sales, q1_net_sales, q4_net_sales, gross_profit, q1_gross_profit, q4_gross_profit, ongoing_operating_income, q1_ongoing_operating_income, q4_ongoing_operating_income
from reports
where code = '005930'
order by rdate desc;

-- 누락된 분기 수 확인
select count(*), count(distinct code)
from reports
where q1_net_sales is null and rdate != '20060331' and rdate > '20180930';

select count(*), count(distinct code)
from reports
where q1_gross_profit is null and rdate != '20060331';

select count(*), count(distinct code)
from reports
where q1_ongoing_operating_income is null and rdate != '20060331';

select count(*), count(distinct code)
from reports
where total_assets is null or total_assets = 0 -- and rdate > '20180930';


-- 회사별 누락건 수 확인

select code, count(*)
from reports
where q1_net_sales is null and rdate != '20060331'
group by code
having count(*) > 1;

-- 총자산 누락건 수 확인
select code, count(*)
from reports
where total_assets = 0
group by code;

select rdate, count(*)
from reports
where total_assets = 0
group by rdate
order by rdate desc;


select * from reports where rdate = '20120630' and total_assets = 0;
select * from reports where code = '007820' and rdate >= '20120630'
order by rdate limit 5;

select * from reports where total_assets is null;
