-- 분기보고서 내용이 0 또는 null 인 데이터

select r.code, c.company, c.industry, count(*) as cnt
from reports r
join companies c on r.code = c.code
where r.net_sales is null or r.net_sales = 0
group by r.code
having count(*) < 20
;


select r.code, c.company, c.industry, count(*) as cnt
from reports r
         join companies c on r.code = c.code
where r.total_assets is null or r.total_assets = 0
group by r.code
;

select count(*) from reports;


select *
from reports
limit 10;

select * from reports where rdate is null order by code;

select * from reports where length(code) != 6;

select * from companies where length(code) != 6;

select * from reports where code is null or rdate is null;

select code, rdate, count(*) as cnt
from reports
group by code, rdate
having count(*) > 1;

-- 다 비어있는 데이터 찾기
select c.company, c.industry, r.*
from reports r
         join companies c on r.code = c.code
where total_assets != 0 and net_sales = 0
;

select *
from reports
where code='005930';

-- 매출액, 매출이익, 순이익 데이터 있는 것
select rdate, count(*) as cnt
from reports
where net_sales is not null and net_sales != 0
    and gross_profit is not null and gross_profit != 0
    and ongoing_operating_income is not null and ongoing_operating_income != 0
group by rdate
order by rdate desc
;

-- 데이터확인
select *
from reports where code='000680'
order by rdate desc;