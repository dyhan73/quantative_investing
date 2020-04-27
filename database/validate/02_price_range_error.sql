select code, count(*)
from prices
where max(ifnull(close, 0), ifnull(adj_close, 0)) < low or max(ifnull(close, 0), ifnull(adj_close, 0)) > high
    and market_cap is not null
group by code
order by code;

select c.company, prices.*
from prices
join companies c on prices.code = c.code
where (max(ifnull(close, 0), ifnull(adj_close, 0)) < low or max(ifnull(close, 0), ifnull(adj_close, 0)) > high)
    and market_cap is not null
    and sdate = '20100930'
;

select max(close, adj_close), *
from prices
where code = '033200'
--     and trading_volume = 0
    and sdate between '20070901' and '20081231'
order by sdate;

select code, substr(sdate, 1, 4) as year,
       max(max(ifnull(close, 0), ifnull(adj_close, 0))) as max,
       min(max(ifnull(close, 0), ifnull(adj_close, 0))) as min
from prices
group by code, substr(sdate, 1, 4)
having max > min * 5 or max * 0.2 > min
order by code, year
;

select *
from prices
where sdate = '20200417';